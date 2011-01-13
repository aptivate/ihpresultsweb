from models import Submission, DPQuestion, AgencyCountries, GovQuestion, Country8DPFix, Country, NotApplicable
import traceback

NA_STR = "__NA__"
def is_not_applicable(val):
    if val == None:
        return False

    val = val.strip().lower()
    variations = [na.variation for na in NotApplicable.objects.all()]
    print variations
    if val in variations:
        return True
    else:
        return False

def float_or_zero(val):
    try:
        return float(val)
    except ValueError:
        return 0

def sum_current_values(qs):
    return sum([float_or_zero(el.latest_value) for el in qs if el.latest_value != None])

def sum_baseline_values(qs):
    return sum([float_or_zero(el.baseline_value) for el in qs if el.baseline_value != None])

def func_8dpfix(qs, agency, q):
    countries = Country8DPFix.objects.filter(agency=agency)
    denom = float(len(countries))
    base_num = len([country for country in countries if country.baseline_progress])
    cur_num = len([country for country in countries if country.latest_progress])

    if denom > 0:
        return base_num / denom * 100, cur_num / denom * 100
    else:
        return None, None

def question_values(qs, agency_or_country, q):
    qs = qs.filter(
        question_number=q, 
    )

    qs = qs.filter(question_number=q)
    assert len(qs) == 1
    
    base_val = qs[0].baseline_value
    cur_val = qs[0].latest_value

    return (base_value, cur_value)

def count_factory(value):
    def count_value(qs, agency_or_country, q):
        qs = qs.filter(
            question_number=q, 
        )

        base_value = qs.filter(
            baseline_value__iexact=value
        ).count()

        cur_value = qs.filter(
            latest_value__iexact=value
        ).count()
        
        return (base_value, cur_value)
    return count_value

def exclude_count_factory(value):
    def count_value(qs, agency_or_country, q):
        qs = qs.filter(
            question_number=q, 
        )

        base_value = qs.exclude(
            baseline_value__iexact=value
        ).count()

        cur_value = qs.exclude(
            latest_value__iexact=value
        ).count()
        
        return (base_value, cur_value)
    return count_value

baseline_watchlist = {
    "1" : ["Burkina Faso", "Burundi", "Djibouti", "DRC", "Ethiopia", "Mozambique", "Nepal", "Nigeria"],
    "17" : ["Burundi", "Djibouti", "DRC", "Nigeria"],
    "18" : ["Burkina Faso", "Djibouti", "Nepal", "Nigeria"],
}

latest_watchlist = {
    "1" : ["Burkina Faso", "Djibouti", "DRC", "Nigeria"],
    "17" : ["Burundi", "Djibouti", "DRC", "Nigeria"],
    "18" : ["Burkina Faso", "Djibouti", "Nigeria"],
}

def is_question_applicable(question, country):
    """
    Checks whether a question is applicable to that particular country
    """
    if type(country) == Country:
        country = country.country

    baseline_applicable = True
    latest_applicable = True

    if question in baseline_watchlist and country in baseline_watchlist[question]:
        baseline_applicable = False

    if question in latest_watchlist and country in latest_watchlist[question]:
        latest_applicable = False

    return baseline_applicable, latest_applicable

def country_perc_factory(value):
    def perc_value(qs, agency, q):
        # In some countries certain processes do not exists
        # the watchlist reduces the denominator if the agency
        # is active in such a country for a particular question
        count_value = count_factory(value)
        base_value, _ = count_value(
            qs.exclude(submission__country__country__in=baseline_watchlist.get(q, [])),
            agency, q
        )

        _, cur_value = count_value(qs.exclude(
            submission__country__country__in=latest_watchlist.get(q, [])), 
            agency, q
        )

        def calc_val(watchlist, val):
            watch = watchlist.get(q, [])
            count_value = count_factory(value)
            countries = [
                country 
                for country in AgencyCountries.objects.get_agency_countries(agency) 
                if country.country not in watch
            ]
            
            num_countries = float(len(countries))
            return val / num_countries * 100 if num_countries > 0 else 0.0
        base_value = calc_val(baseline_watchlist, base_value)
        cur_value = calc_val(latest_watchlist, cur_value)

        return base_value, cur_value
    return perc_value

def equals_or_zero(val):
    def test(qs, agency_or_country, q):
        value = val.lower()
        
        qs = qs.filter(question_number=q)
        # TODO not sure what to do here
        #if len(qs) != 1:
        #    return 0, 0
        try:
            assert len(qs) == 1
            
            if qs[0].baseline_value == None:
                base_val = 0
            else:
                base_val = 100 if qs[0].baseline_value.lower() == value else 0

            if qs[0].latest_value == None:
                cur_val = 0
            else:
                cur_val = 100 if qs[0].latest_value.lower() == value else 0
            return base_val, cur_val
        except AssertionError:
            return None, None
    return test

def equals_yes_or_no(val):
    def test(qs, agency_or_country, q):
        value = val.lower()
        
        qs = qs.filter(question_number=q)
        # TODO not sure what to do here
        #if len(qs) != 1:
        #    return 0, 0
        assert len(qs) == 1
        
        if qs[0].baseline_value == None:
            base_val = ""
        else:
            base_val = "y" if qs[0].baseline_value.lower() == value else "n"

        if qs[0].latest_value == None:
            cur_val = ""
        else:
            cur_val = "y" if qs[0].latest_value.lower() == value else "n"
        return base_val, cur_val
    return test

def combine_yesnos(qs, agency_or_country, *args):
    values_baseline = []
    values_current = []
    for arg in args:
        qs1 = qs.filter(question_number=arg)
        #if qs1.count() == 0:
        #    values_baseline.append(" ")
        #    values_current.append(" ")
        #    continue
        if qs1[0].baseline_value == None:
            base_val = " "
        else: 
            base_val = "y" if qs1[0].baseline_value.lower() == "yes" else "n"

        if qs1[0].latest_value == None:
            cur_val = " "
        else:
            cur_val = "y" if qs1[0].latest_value.lower() == "yes" else "n"

        values_baseline.append(base_val)
        values_current.append(cur_val)
    return "".join(values_baseline), "".join(values_current)

def calc_numdenom(qs, agency_or_country, numq, denomq):
    cur_den = float(sum_current_values(qs.filter(question_number=denomq)))
    cur_num = float(sum_current_values(qs.filter(question_number=numq)))
    base_den = float(sum_baseline_values(qs.filter(question_number=denomq)))
    base_num = float(sum_baseline_values(qs.filter(question_number=numq)))

    base_ratio = cur_ratio = None
    if base_den > 0: base_ratio = base_num / base_den * 100
    if cur_den > 0: cur_ratio = cur_num / cur_den * 100
    return (base_ratio, cur_ratio)

def calc_one_minus_numdenom(qs, agency_or_country, numq, denomq):
    (base_ratio, cur_ratio) = calc_numdenom(qs, agency_or_country, numq, denomq)
    base_ratio = 100 - base_ratio if base_ratio != None else None
    cur_ratio = 100 - cur_ratio if cur_ratio != None else None
    
    return base_ratio, cur_ratio

def sum_values(qs, agency_or_country, *args):
    qs = qs.filter(question_number__in=args)

    cur_val = float(sum_current_values(qs))
    base_val = float(sum_baseline_values(qs))

    return (base_val, cur_val)

def calc_indicator(qs, agency_or_country, indicator, funcs=None):
    funcs = funcs or indicator_funcs
    func, args = funcs[indicator]
    # TODO - this is really ugly - probably need to refactor this code
    qs2 = qs.filter(question_number__in=args)
    
    comments = [(question.question_number, question.submission.country, question.comments) for question in qs2]

    exclude = []
    for q in qs2:
        baseline_applicable, latest_applicable = is_question_applicable(q.question_number, q.submission.country)
        if is_not_applicable(q.baseline_value) or is_not_applicable(q.latest_value):
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
    currently only calculating for 2DPa, 2DPb, 2DPc, 5DPa, 5DPb

    """
    indicators = ["2DPa", "2DPb", "2DPc", "5DPa", "5DPb"]
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

positive_funcs = dict(indicator_funcs)
positive_funcs["2DPa"] = (calc_numdenom, ("3", "2"))
positive_funcs["4DP"] = (calc_numdenom, ("11", "10"))
positive_funcs["5DPa"] = (calc_numdenom, ("13", "12"))
positive_funcs["5DPb"] = (calc_numdenom, ("15", "14"))
positive_funcs["4G"] = (calc_numdenom, ("8", "7"))
