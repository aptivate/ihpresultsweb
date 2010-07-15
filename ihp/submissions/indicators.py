from models import Submission, DPQuestion, AgencyCountries

def sum_current_values(qs):
    return sum([int(el.latest_value) for el in qs])

def sum_baseline_values(qs):
    return sum([int(el.baseline_value) for el in qs])

def count_factory(value):
    def count_value(qs, q):
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
    def count_value(qs, q):
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

def perc_factory(value):
    def perc_value(qs, q):
        count_value = count_factory(value)
        exclude_count_value = exclude_count_factory(value)

        base_value, cur_value = count_value(qs, q)
        base_exclude_value, cur_exclude_value = exclude_count_value(qs, q)


        return (float(base_value) / (base_value + base_exclude_value), float(cur_value) / (cur_value + cur_exclude_value))
    return perc_value

def calc_numdenom(qs, numq, denomq):
    cur_den = float(sum_current_values(qs.filter(question_number=denomq)))
    cur_num = float(sum_current_values(qs.filter(question_number=numq)))
    base_den = float(sum_baseline_values(qs.filter(question_number=denomq)))
    base_num = float(sum_baseline_values(qs.filter(question_number=numq)))

    base_ratio = cur_ratio = 0 # TODO this is an intentional bug - it makes life so much easier
    if base_den > 0: base_ratio = base_num / base_den
    if cur_den > 0: cur_ratio = cur_num / cur_den
    return (base_ratio, cur_ratio)

def sum_values(qs, q):
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

def calc_indicator(qs, indicator):
    func, args = indicator_funcs[indicator]
    qs2 = qs.filter(question_number__in=args)
    comments = [(question.question_number, question.submission.country, question.comments) for question in qs2]
    return func(qs, *args), comments

def calc_agency_indicator(agency, indicator):
    qs = DPQuestion.objects.filter(submission__agency=agency)
    return calc_indicator(qs, indicator)

def calc_agency_indicators(agency):
    results = [calc_agency_indicator(agency, indicator) for indicator in indicators]
    return dict(zip(indicators, results))

indicators = [
    "1DP" , "2DPa", "2DPb",
    "2DPc", "3DP" , "4DP" ,
    "5DPa", "5DPb", "5DPc",
    "6DP" , "7DP" , "8DP" ,
]

indicator_funcs = {
    "1DP"  : (perc_factory("yes"), ("1",)),
    "2DPa" : (calc_numdenom, ("3", "2")),
    "2DPb" : (calc_numdenom, ("5", "4")),
    "2DPc" : (calc_numdenom, ("6", "2")),
    "3DP"  : (calc_numdenom, ("7", "2")),
    "4DP"  : (calc_numdenom, ("8b", "8")),
    "5DPa" : (calc_numdenom, ("10", "9")),
    "5DPb" : (calc_numdenom, ("12", "9")),
    "5DPc" : (sum_values, ("13",)),
    "6DP"  : (count_factory("yes"), ("15",)),
    "7DP"  : (count_factory("yes"), ("16",)),
    "8DP"  : (count_factory("yes"), ("17",)),
}

