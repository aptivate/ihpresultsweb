from models import Submission, DPQuestion, AgencyCountries

def sum_current_values(qs):
    return sum([int(el.latest_value) for el in qs])

def sum_baseline_values(qs):
    return sum([int(el.baseline_value) for el in qs])

def count_yes(qs, q):
    qs = qs.filter(
        question_number=q, 
    )

    base_yes = qs.filter(
        baseline_value__iexact="yes"
    ).count()

    cur_yes = qs.filter(
        latest_value__iexact="yes"
    ).count()
    
    return (base_yes, cur_yes)

def calc_numdenom(qs, numq, denomq):
    cur_den = float(sum_current_values(qs.filter(question_number=denomq)))
    cur_num = float(sum_current_values(qs.filter(question_number=numq)))
    base_den = float(sum_baseline_values(qs.filter(question_number=denomq)))
    base_num = float(sum_baseline_values(qs.filter(question_number=numq)))
    return (base_num / base_den, cur_num / cur_den)

def sum_values(qs, q):
    qs = qs.filter(question_number=q)

    cur_val = float(sum_current_values(qs))
    base_val = float(sum_baseline_values(qs))

    return (base_val, cur_val)


def calc_dp_indicator(agency, indicator):
    qs = DPQuestion.objects.filter(
       submission__agency=agency, 
    )

    return calc_indicator(qs, indicator)

def calc_country_indicator(country, indicator):
    qs = DPQuestion.objects.filter(
       submission__country=country, 
    )

    return calc_indicator(qs, indicator)

def calc_indicator(qs, indicator):
    
    indicators = {
        "1DP"  : (count_yes, ("1",)),
        "2DPa" : (calc_numdenom, ("3", "2")),
        "2DPb" : (calc_numdenom, ("5", "4")),
        "2DPc" : (calc_numdenom, ("6", "2")),
        "3DP"  : (calc_numdenom, ("7", "2")),
        "4DP"  : (calc_numdenom, ("8b", "8")),
        "5DPa" : (calc_numdenom, ("10", "9")),
        "5DPb" : (calc_numdenom, ("12", "9")),
        "5DPc" : (sum_values, ("13",)),
        "6DP"  : (count_yes, ("15",)),
        "7DP"  : (count_yes, ("16",)),
        "8DP"  : (count_yes, ("17",)),
    }

    if indicator in indicators:
        func, args = indicators[indicator]
        return func(qs, *args)
