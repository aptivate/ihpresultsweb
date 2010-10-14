from indicators import calc_agency_indicators, calc_country_indicators, dp_indicators, g_indicators, calc_agency_country_indicators
from models import AgencyTargets, AgencyCountries, Submission, CountryTargets
import math

def criterion_absolute(base_val, cur_val, criterion_param):
    
    if cur_val == None: return None
    if math.fabs(cur_val - criterion_param) < 0.000000001:
        return True
    return False

def criterion_relative_increase(base_val, cur_val, criterion_param):
    if cur_val == None or base_val == None: return None
    if cur_val >= base_val * (1 + criterion_param / 100.0):
        return True
    return False

def criterion_relative_decrease(base_val, cur_val, criterion_param):
    if cur_val == None or base_val == None: return None

    if cur_val <= base_val * (1 - criterion_param / 100.0):
        return True
    return False

def criterion_increase(base_val, cur_val, criterion_param):
    if cur_val == None or base_val == None: return None

    if cur_val > base_val:
        return True
    return False

def criterion_decrease(base_val, cur_val, criterion_param):
    if cur_val == None or base_val == None: return None

    if cur_val < base_val:
        return True
    return False

def criterion_absolute_greater_than(base_val, cur_val, criterion_param):
    if cur_val == None: return None
    if cur_val > criterion_param:
        return True
    return False

def criterion_absolute_less_than(base_val, cur_val, criterion_param):
    if cur_val == None: return None
    if cur_val < criterion_param:
        return True
    return False

def criterion_absolute_increase(base_val, cur_val, criterion_param):
    if cur_val - criterion_param > base_val:
        return True
    return False

def criterion_absolute_decrease(base_val, cur_val, criterion_param):
    if cur_val + criterion_param < base_val:
        return True
    return False

def criterion_both_yes(base_val, cur_val, criterion_param):
    if cur_val.lower() == "yy":
        return True
    return False

def criterion_first_yes(base_val, cur_val, criterion_param):
    if cur_val.lower()[0] == "y":
        return True
    return False

criteria_funcs = {
   "Absolute % Target" : criterion_absolute,
   "Minimum x% Increase relative to baseline" : criterion_relative_increase,
   "Minimum x% Decrease relative to baseline" : criterion_relative_decrease,
   "Increase relative to baseline (no minimum)" : criterion_increase,
   "Decrease relative to baseline (no minimum)" : criterion_decrease,
   "Absolute greater than x%" : criterion_absolute_greater_than,
   "Absolute less than x%" : criterion_absolute_less_than,
   "Absolute Value Increase" : criterion_absolute_increase,
   "Absolute Value Decrease" : criterion_absolute_decrease,
   "Both Questions Yes" : criterion_both_yes,
   "First Question Yes" : criterion_first_yes,
}

def get_agency_targets(agency, indicators):
    targets = {}
    for indicator in indicators:
        try:
            target = AgencyTargets.objects.get(agency=agency, indicator=indicator)
        except AgencyTargets.DoesNotExist:
            target = AgencyTargets.objects.get(agency=None, indicator=indicator)
        targets[indicator] = target
    return targets

def get_country_targets(country, indicators):
    targets = {}
    for indicator in indicators:
        try:
            target = CountryTargets.objects.get(country=country, indicator=indicator)
        except CountryTargets.DoesNotExist:
            target = CountryTargets.objects.get(country=None, indicator=indicator)
        targets[indicator] = target
    return targets

def none_sub(a, b):
    if a == None or b == None:
        return None
    return a - b

def none_mul(a, b):
    if a == None or b == None:
        return None
    return a * b

def evaluate_indicator(target, base_val, cur_val):
    tick_func = criteria_funcs[target.tick_criterion_type]
    arrow_func = criteria_funcs[target.arrow_criterion_type]

    if tick_func(base_val, cur_val, target.tick_criterion_value):
        return "tick"
    elif arrow_func(base_val, cur_val, target.arrow_criterion_value):
        return "arrow"
    else:
        return "cross"

def calc_agency_targets(agency):
    """
    Returns information for all indicators for the given agency in a dict with the
    following form
    {
        "1DP" : {
            "base_val" : ...,
            "cur_val" : ...,
            "comments" : ...,
            "target" : ...,
        },
        "2DPa" : {
            "base_val" : ...,
            "cur_val" : ...,
            "comments" : ...,
            "target" : ...,
        },
        .
        .
        .
    }
    """

    commentary_map = {
        "1DP" : "An IHP+ Country Compact or equivalent was signed in %(cur_val)d%% of IHP+ countries where these exist, by the end of %(cur_year)s. Target = %(target_val)d%% of IHP+ countries where the signatory operates have support for/commitment to the IHP+ compact (or equivalent) mutually agreed and documented.",
        "2DPa" : "%(cur_val)d%% of health sector aid was reported on national health sector budgets by the end of %(cur_year)s - %(diff_direction)s from %(base_val)d%% in 2006. Target %(target_val)d%%.",
        "2DPb" :"%(cur_val)d%% of capacity development support was provided through co-ordinated programmes in %(cur_year)s - %(diff_direction)s from %(base_val)d%% in %(base_year)s. Target = %(target_val)d%%",
        "2DPc" : "%(cur_val)d%% of health sector aid was provided through programme based approaches by the end of %(cur_year)s, %(diff_direction)s of %(diff_val)d%% from the %(base_year)s baseline. Target = %(target_val)d%%.",
        "3DP" : "%(cur_val)d%% of health sector funding was provided through multi-year commitments by the end of %(cur_year)s: %(diff_direction)s from %(base_val)d%% in %(base_year)s. Target = %(target_val)d%%.",
        "4DP" : "In %(cur_year)s, %(cur_val)d%% of health sector aid disbursements were released according to agreed schedules in annual or multi-year frameworks - %(diff_direction)s from %(base_val)d%% in %(base_year)s.",
        "5DPa" : "By the end of %(cur_year)s, %(cur_val)d%% of health sector aid used government partner country public financial management systems: %(diff_direction)s from %(base_val)d%% since %(base_year)s. Target = %(target_val)d%% of aid to be chanelled through partner country PFM systems.",
        "5DPb" : "By end %(cur_year)s, %(one_minus_cur_val)d%% of health sector aid used country procurement systems in IHP+ partner countries: %(one_minus_diff_direction)s from %(one_minus_base_val)d%% in %(base_year)s. Target = %(one_minus_target_val)d%% reduction in the %% of health sector aid to the public sector not useing partner country procurement systems.",
        "5DPc" : "There are no more than %(cur_val)d parallel Project Implementation Units (PIUs) in any IHP+ country: %(diff_direction2)s from %(base_val)d in %(base_year)s. Target = reduce the stock of PIUs to %(target_val)d.",
        "6DP" : "Where they exist, national performance assessment frameworks are used to assess progress in %(cur_val)d%% of IHP+ countries: increased from %(base_val)d%% in %(base_year)s. Target = %(target_val)s%%.",
        "7DP" : "Participated in annual mutual assessments of progress in implementing health sector commitments & agreements (such as the IHP+ country compact and on aid effectiveness in the health sector) in all IHP+ countries. Target = %(target_val)d%%.",
        "8DP" : "",
    }
        
    targets = get_agency_targets(agency, dp_indicators)
    indicators = calc_agency_indicators(agency)
    results = {}
    for indicator in indicators:
        (base_val, base_year, cur_val, cur_year), comments = indicators[indicator]
        target = targets[indicator]

        result = {
            "base_val" : base_val,
            "base_year" : base_year,
            "cur_val" : cur_val,
            "cur_year" : cur_year,
            "comments" : comments,
            "commentary" : "",
        }

        result["target"] = evaluate_indicator(target, base_val, cur_val)

        # create commentary
        if base_val != None and cur_val != None:
            result["diff_val"] = math.fabs(base_val - cur_val)
            result["diff_direction"] = "a decrease" if base_val - cur_val > 0 else "an increase"
            result["diff_direction2"] = "down" if base_val - cur_val > 0 else "up"
            result["target_val"] = target.tick_criterion_value
            if target.tick_criterion_type == "Minimum x% Decrease relative to baseline":
                result["target_val"] = (1 - target.tick_criterion_value / 100.0) * base_val
            elif target.tick_criterion_type == "Minimum x% Increase relative to baseline":
                result["target_val"] = (1 + target.tick_criterion_value / 100.0) * base_val
            result["one_minus_base_val"] = 100 - result["base_val"]
            result["one_minus_cur_val"] = 100 - result["cur_val"]
            if result["target_val"]:
                result["one_minus_target_val"] = 100 - result["target_val"]
            else:
                result["one_minus_target_val"] = None
        
            result["one_minus_diff_direction"] = "a decrease" if base_val - cur_val < 0 else "an increase"

            result["commentary"] = commentary_map[indicator] % result

        results[indicator] = result

    return results

def calc_country_targets(country):
    """
    Returns information for all indicators for the given country in a dict with the
    following form
    {
        "1G" : {
            "base_val" : ...,
            "cur_val" : ...,
            "comments" : ...,
            "target" : ...,
        },
        "2Ga" : {
            "base_val" : ...,
            "cur_val" : ...,
            "comments" : ...,
            "target" : ...,
        },
        .
        .
        .
    }
    """
    targets = get_country_targets(country, g_indicators)
    indicators = calc_country_indicators(country)
    results = {}
    for indicator in indicators:
        (base_val, base_year, cur_val, cur_year), comments = indicators[indicator]
        target = targets[indicator]

        result = {
            "base_val" : base_val,
            "base_year" : base_year,
            "cur_val" : cur_val,
            "cur_year" : cur_year,
            "comments" : comments,
            "commentary" : "",
        }

        result["target"] = evaluate_indicator(target, base_val, cur_val)
        results[indicator] = result

    return results

def get_country_progress(agency):
    np = []
    p = []
    np_dict = {}
    p_dict = {}
    targets = get_agency_targets(agency, dp_indicators)
    for country in AgencyCountries.objects.get_agency_countries(agency):
        country_indicators = calc_agency_country_indicators(agency, country)
        if Submission.objects.filter(agency=agency, country=country).count() == 0:
            np.append(country)
        else:
            num_indicators = ticks = 0
            for indicator in country_indicators:
                (base_val, base_year, cur_val, cur_year), comments = country_indicators[indicator]
                # TODO this is a hack - it might be better to extract this
                # logic out of here
                result = "cross"
                if indicator in ["1DP", "6DP", "7DP", "8DP"]:
                    if cur_val > 0: result = "tick" 
                else:
                    target = targets[indicator]
                    result = evaluate_indicator(target, base_val, cur_val)
                if result != "cross":
                    ticks += 1.0
                num_indicators += 1.0
            if ticks / num_indicators > 0.5:
                p.append(country)
            else:
                np.append(country)
    for i, country in enumerate(sorted(p)):
        p_dict[i + 1] = country
    for i, country in enumerate(sorted(np)):
        np_dict[i + 1] = country
        
    return np_dict, p_dict

def get_agency_progress(country):
    np = []
    p = []
    np_dict = {}
    p_dict = {}
    for agency in AgencyCountries.objects.get_country_agencies(country):
        targets = get_agency_targets(agency, dp_indicators)
        country_indicators = calc_agency_country_indicators(agency, country)
        if Submission.objects.filter(agency=agency, country=country).count() == 0:
            np.append(agency)
        else:
            num_indicators = ticks = 0
            for indicator in country_indicators:
                (base_val, base_year, cur_val, cur_year), comments = country_indicators[indicator]
                # TODO this is a hack - it might be better to extract this
                # logic out of here
                result = "cross"
                if indicator in ["1DP", "6DP", "7DP", "8DP"]:
                    if cur_val > 0: result = "tick" 
                else:
                    target = targets[indicator]
                    result = evaluate_indicator(target, base_val, cur_val)
                if result != "cross":
                    ticks += 1.0
                num_indicators += 1.0
            if ticks / num_indicators > 0.5:
                p.append(agency)
            else:
                np.append(agency)
    for i, agency in enumerate(sorted(p)):
        p_dict[i + 1] = agency
    for i, agency in enumerate(sorted(np)):
        np_dict[i + 1] = agency
        
    return np_dict, p_dict
