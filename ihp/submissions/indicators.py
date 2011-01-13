from models import Submission, DPQuestion, AgencyCountries, GovQuestion, Country8DPFix, Country, NotApplicable, CountryExclusion
from indicator_funcs import *
import traceback

NA_STR = "__NA__"

def calc_indicator(qs, agency_or_country, indicator, funcs=None):
    funcs = funcs or indicator_funcs
    func, args = funcs[indicator]
    # TODO - this is really ugly - probably need to refactor this code
    qs2 = qs.filter(question_number__in=args)
    
    comments = [(question.question_number, question.submission.country, question.comments) for question in qs2]

    exclude = []
    for q in qs2:
        if type(q) == DPQuestion:
            baseline_applicable, latest_applicable = CountryExclusion.objects.is_applicable(q.question_number, q.submission.country)
        else:
            baseline_applicable, latest_applicable = True, True

        if NotApplicable.objects.is_not_applicable(q.baseline_value) or NotApplicable.objects.is_not_applicable(q.latest_value):
            exclude.append(q.submission.id)
        elif not baseline_applicable or not latest_applicable:
            exclude.append(q.submission.id)
    qs2 = qs2.exclude(submission__id__in=exclude)
        
    if qs2.count() == 0:
        base_val, cur_val = NA_STR, NA_STR
    else:
        base_val, cur_val = func(qs, agency_or_country, *args)
    
    # TODO here i assume that the year is the same across all years and all questions. 
    if len(qs2) > 0: 
        cur_year = qs2[0].latest_year
        base_year = qs2[0].baseline_year
    else:
        cur_year = base_year = None

    return (base_val, base_year, cur_val, cur_year), comments

def calc_agency_indicator(agency, indicator):
    """
    Calculate the value of a particular indicator for the given agency
    Returns a tuple ((base_val, base_year, cur_val, cur_year), indicator comment)
    """
    qs = DPQuestion.objects.filter(submission__agency=agency)
    return calc_indicator(qs, agency, indicator)

def calc_agency_indicators(agency):
    """
    Calculates all the indicators for the given agency
    Returns a dict with the following form
    {
        "1DP" : ((base_1dp, base_1dp_year, cur_1dp, cur_1dp_year), comment_1dp),
        "2DPa" : ((base_2dpa, base_2dpa_year, cur_2dpa, cur_2dpa_year), comment_2dp),
        .
        .
        .
    }
    """
    results = [calc_agency_indicator(agency, indicator) for indicator in dp_indicators]
    return dict(zip(dp_indicators, results))

def calc_overall_agency_indicators(funcs=None):
    """
    Calculates all indicators aggregated across all agencies and agencycountries
    i.e. there will be two values per indicator, baseline value and latest value
    currently only calculating for 2DPa, 2DPb, 2DPc, 3DP, 5DPa, 5DPb, 5DPc

    """
    indicators = ["2DPa", "2DPb", "2DPc", "3DP", "5DPa", "5DPb", "5DPc"]
    qs = DPQuestion.objects.all()

    results = [calc_indicator(qs, None, indicator, funcs) for indicator in indicators]
    return dict(zip(indicators, results))

def calc_agency_country_indicator(agency, country, indicator, funcs=None):
    """
    Same as calc_agency_indicator above but only looks at a specific country
    """
    qs = DPQuestion.objects.filter(submission__agency=agency, submission__country=country)
    funcs = funcs or dict(indicator_funcs)
    try:
        funcs["1DP"] = (equals_or_zero("yes"), ("1",))
        funcs["6DP"] = (equals_or_zero("yes"), ("17",))
        funcs["7DP"] = (equals_or_zero("yes"), ("18",))
        funcs["8DP"] = (equals_or_zero("yes"), ("20",))
        return calc_indicator(qs, agency, indicator, funcs)
    except:
        traceback.print_exc()
        

def calc_agency_country_indicators(agency, country, funcs=None):
    """
    Same as calc_agency_indicators above but only looks at a specific country
    """
    results = [calc_agency_country_indicator(agency, country, indicator, funcs) for indicator in dp_indicators]
    return dict(zip(dp_indicators, results))

def calc_country_indicator(country, indicator, funcs=None):
    """
    Calculate the value of a particular indicator for the given country
    Returns a tuple ((base_val, base_year, cur_val, cur_year), indicator comment)
    """
    qs = GovQuestion.objects.filter(submission__country=country)
    return calc_indicator(qs, country, indicator, funcs)

def calc_country_indicators(country, funcs=None):
    """
    Calculates all the indicators for the given agency
    Returns a dict with the following form
    {
        "1G" : ((base_1g, base_1g_year, cur_1g, cur_1g_year), comment_1g),
        "2DPa" : ((base_2ga, base_2ga_year, cur_2ga, cur_2ga_year), comment_2g),
        .
        .
        .
    }
    """
    results = [calc_country_indicator(country, indicator, funcs) for indicator in g_indicators]
    return dict(zip(g_indicators, results))

dp_indicators = [
    "1DP" , "2DPa", "2DPb",
    "2DPc", "3DP" , "4DP" ,
    "5DPa", "5DPb", "5DPc",
    "6DP" , "7DP" , "8DP" ,
]

g_indicators = [
    "1G" , "2Ga", "2Gb",
    "3G" , "4G", "5Ga", "5Gb",
    "6G" , "7G", "8G",
    "Q2G", "Q3G",
    "Q12G", "Q21G",
]

#TODO do checks to ensure that questions that aren't answered to break anything
indicator_funcs = {
    "1DP"  : (country_perc_factory("yes"), ("1",)),
    "2DPa" : (calc_one_minus_numdenom, ("3", "2")),
    "2DPb" : (calc_numdenom, ("5", "4")),
    "2DPc" : (calc_numdenom, ("7", "6")),
    "3DP"  : (calc_numdenom, ("9", "8")),
    "4DP"  : (calc_one_minus_numdenom, ("11", "10")),
    "5DPa" : (calc_one_minus_numdenom, ("13", "12")),
    "5DPb" : (calc_one_minus_numdenom, ("15", "14")),
    "5DPc" : (sum_values, ("16",)),
    "6DP"  : (country_perc_factory("yes"), ("17",)),
    "7DP"  : (country_perc_factory("yes"), ("18",)),
    "8DP"  : (func_8dpfix, ("20",)),
    "1G"   : (equals_yes_or_no("yes"), ("1",)),
    "2Ga"  : (combine_yesnos, ("2", "3")),
    "2Gb"  : (equals_or_zero("yes"), ("4",)),
    "3G"   : (calc_numdenom, ("6", "5")),
    "4G"   : (calc_one_minus_numdenom, ("8", "7")),
    "5Ga"  : (sum_values, ("9",)),
    "5Gb"  : (sum_values, ("10",)),
    "6G"   : (equals_yes_or_no("yes"), ("11",)),
    "7G"   : (equals_yes_or_no("yes"), ("12",)),
    "8G"   : (calc_numdenom, ("13", "14")),
    "Q2G" : (equals_yes_or_no("yes"), ("2",)),
    "Q3G" : (equals_yes_or_no("yes"), ("3",)),
    "Q12G" : (equals_yes_or_no("yes"), ("12",)),
    "Q21G" : (equals_yes_or_no("yes"), ("21",)),
}

# Functions that calculate values in a positive sense - i.e. how much on budget, not how much off budget
positive_funcs = dict(indicator_funcs)
positive_funcs["2DPa"] = (calc_numdenom, ("3", "2"))
positive_funcs["4DP"] = (calc_numdenom, ("11", "10"))
positive_funcs["5DPa"] = (calc_numdenom, ("13", "12"))
positive_funcs["5DPb"] = (calc_numdenom, ("15", "14"))
positive_funcs["4G"] = (calc_numdenom, ("8", "7"))
