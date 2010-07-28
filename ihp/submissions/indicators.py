from models import Submission, DPQuestion, AgencyCountries

def sum_current_values(qs):
    return sum([int(el.latest_value) for el in qs])

def sum_baseline_values(qs):
    return sum([int(el.baseline_value) for el in qs])

def count_factory(value):
    def count_value(qs, agency, q):
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
    def count_value(qs, agency, q):
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

def calc_numdenom(qs, agency, numq, denomq):
    cur_den = float(sum_current_values(qs.filter(question_number=denomq)))
    cur_num = float(sum_current_values(qs.filter(question_number=numq)))
    base_den = float(sum_baseline_values(qs.filter(question_number=denomq)))
    base_num = float(sum_baseline_values(qs.filter(question_number=numq)))

    base_ratio = cur_ratio = None
    if base_den > 0: base_ratio = base_num / base_den * 100
    if cur_den > 0: cur_ratio = cur_num / cur_den * 100
    return (base_ratio, cur_ratio)

def sum_values(qs, agency, q):
    qs = qs.filter(question_number=q)

    cur_val = float(sum_current_values(qs))
    base_val = float(sum_baseline_values(qs))

    return (base_val, cur_val)


#def calc_country_indicator(country, indicator):
#    qs = DPQuestion.objects.filter(
#       submission__country=country, 
#    )
#
#    return calc_indicator(qs, indicator)

def calc_indicator(qs, agency, indicator):
    func, args = indicator_funcs[indicator]
    # TODO - this is really ugly - probably need to refactor this code
    qs2 = qs.filter(question_number__in=args)
    comments = [(question.question_number, question.submission.country, question.comments) for question in qs2]
    base_val, cur_val = func(qs, agency, *args)
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
    results = [calc_agency_indicator(agency, indicator) for indicator in indicators]
    return dict(zip(indicators, results))

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
    results = [calc_agency_country_indicator(agency, country, indicator) for indicator in indicators]
    return dict(zip(indicators, results))

indicators = [
    "1DP" , "2DPa", "2DPb",
    "2DPc", "3DP" , "4DP" ,
    "5DPa", "5DPb", "5DPc",
    "6DP" , "7DP" , "8DP" ,
]

indicator_funcs = {
    "1DP"  : (country_perc_factory("yes"), ("1",)),
    "2DPa" : (calc_numdenom, ("3", "2")),
    "2DPb" : (calc_numdenom, ("5", "4")),
    "2DPc" : (calc_numdenom, ("6", "2")),
    "3DP"  : (calc_numdenom, ("7", "2")),
    "4DP"  : (calc_numdenom, ("8b", "8")),
    "5DPa" : (calc_numdenom, ("10", "9")),
    "5DPb" : (calc_numdenom, ("12", "9")),
    "5DPc" : (sum_values, ("13",)),
    "6DP"  : (country_perc_factory("yes"), ("15",)),
    "7DP"  : (country_perc_factory("yes"), ("16",)),
    "8DP"  : (country_perc_factory("yes"), ("17",)),
}

