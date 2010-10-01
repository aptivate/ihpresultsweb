from models import Submission, DPQuestion, AgencyCountries, GovQuestion

def float_or_zero(val):
    try:
        return float(val)
    except ValueError:
        return 0

def sum_current_values(qs):
    return sum([float_or_zero(el.latest_value) for el in qs if el.latest_value != None])

def sum_baseline_values(qs):
    return sum([float_or_zero(el.baseline_value) for el in qs if el.baseline_value != None])

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

def country_perc_factory(value):
    def perc_value(qs, agency, q):
        count_value = count_factory(value)

        base_value, cur_value = count_value(qs, agency, q)
        num_countries = float(len(AgencyCountries.objects.get_agency_countries(agency)))
        if num_countries == 0:
            return None, None
        else:
            return (base_value / num_countries * 100), (cur_value / num_countries * 100)
    return perc_value

def equals_or_zero(val):
    def test(qs, agency_or_country, q):
        value = val.lower()
        
        qs = qs.filter(question_number=q)
        assert len(qs) == 1
        
        base_val = 100 if qs[0].baseline_value.lower() == value else 0
        cur_val = 100 if qs[0].latest_value.lower() == value else 0
        return base_val, cur_val
    return test

def combine_yesnos(qs, agency_or_country, *args):
    values_baseline = []
    values_current = []
    for arg in args:
        qs1 = qs.filter(question_number=arg)
        base_val = "y" if qs1[0].baseline_value.lower() == "yes" else "n"
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
    if base_ratio and cur_ratio:
        return (100 - base_ratio, 100 - cur_ratio)
    else:
        return base_ratio, cur_ratio

def sum_values(qs, agency_or_country, *args):
    qs = qs.filter(question_number__in=args)

    cur_val = float(sum_current_values(qs))
    base_val = float(sum_baseline_values(qs))

    return (base_val, cur_val)


#def calc_country_indicator(country, indicator):
#    qs = DPQuestion.objects.filter(
#       submission__country=country, 
#    )
#
#    return calc_indicator(qs, indicator)

def calc_indicator(qs, agency_or_country, indicator):
    func, args = indicator_funcs[indicator]
    # TODO - this is really ugly - probably need to refactor this code
    qs2 = qs.filter(question_number__in=args)
    comments = [(question.question_number, question.submission.country, question.comments) for question in qs2]
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
    print "Agency: %s" % agency
    print "Indicator: %s"  % indicator
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

def calc_agency_country_indicator(agency, country, indicator):
    """
    Same as calc_agency_indicator above but only looks at a specific country
    """
    qs = DPQuestion.objects.filter(submission__agency=agency, submission__country=country)
    return calc_indicator(qs, agency, indicator)

def calc_agency_country_indicators(agency, country):
    """
    Same as calc_agency_indicators above but only looks at a specific country
    """
    results = [calc_agency_country_indicator(agency, country, indicator) for indicator in dp_indicators]
    return dict(zip(dp_indicators, results))

def calc_country_indicator(country, indicator):
    """
    Calculate the value of a particular indicator for the given country
    Returns a tuple ((base_val, base_year, cur_val, cur_year), indicator comment)
    """
    qs = GovQuestion.objects.filter(submission__country=country)
    return calc_indicator(qs, country, indicator)

def calc_country_indicators(country):
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
    results = [calc_country_indicator(country, indicator) for indicator in g_indicators]
    return dict(zip(g_indicators, results))

dp_indicators = [
    "1DP" , "2DPa", "2DPb",
    "2DPc", "3DP" , "4DP" ,
    "5DPa", "5DPb", "5DPc",
    "6DP" , "7DP" , "8DP" ,
]

g_indicators = [
    "1G" , "2Ga", "2Gb",
    "3G" , "4G", "5G",
    "6G" , "7G", "8G",
]

#TODO do checks to ensure that questions that aren't answered to break anything
indicator_funcs = {
    "1DP"  : (country_perc_factory("yes"), ("1",)),
    "2DPa" : (calc_numdenom, ("3", "2")),
    "2DPb" : (calc_numdenom, ("5", "4")),
    "2DPc" : (calc_numdenom, ("7", "6")),
    "3DP"  : (calc_numdenom, ("9", "8")),
    "4DP"  : (calc_one_minus_numdenom, ("11", "10")),
    "5DPa" : (calc_one_minus_numdenom, ("13", "12")),
    "5DPb" : (calc_one_minus_numdenom, ("15", "14")),
    "5DPc" : (sum_values, ("16",)),
    "6DP"  : (country_perc_factory("yes"), ("17",)),
    "7DP"  : (country_perc_factory("yes"), ("18",)),
    "8DP"  : (country_perc_factory("yes"), ("20",)),
    "1G"   : (equals_or_zero("yes"), ("1",)),
    "2Ga"  : (combine_yesnos, ("2", "3")),
    "2Gb"  : (equals_or_zero("yes"), ("4",)),
    "3G"   : (calc_numdenom, ("6", "5")),
    "4G"   : (calc_one_minus_numdenom, ("8", "7")),
    "5G"   : (sum_values, ("9", "10")),
    "6G"   : (equals_or_zero("yes"), ("11",)),
    "7G"   : (equals_or_zero("yes"), ("12",)),
    "8G"   : (calc_numdenom, ("13", "14")),
}
