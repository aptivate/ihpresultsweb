from indicators import calc_agency_indicators, indicators
from models import Targets
import math

def criterion_absolute(base_val, cur_val, criterion_param):
    
    if cur_val == None: return None
    if cur_val * 100 - criterion_param < 0.000000001:
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

criteria_funcs = {
   "Absolute % Target" : criterion_absolute,
   "Minimum x% Increase relative to baseline" : criterion_relative_increase,
   "Minimum x% Decrease relative to baseline" : criterion_relative_decrease,
   "Increase relative to baseline (no minimum)" : criterion_increase,
   "Decrease relative to baseline (no minimum)" : criterion_decrease,
}

def get_agency_targets(agency):
    targets = {}
    for indicator in indicators:
        try:
            target = Targets.objects.get(agency=agency, indicator=indicator)
        except Targets.DoesNotExist:
            target = Targets.objects.get(agency=None, indicator=indicator)
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
        "2DPa" : "%(cur_val)d%% of health sector aid was reported on national health sector budgets by the end of %(cur_year)s - %(diff_direction)s from %(base_val)d%% in 2006. Target %(target_val)s.",
        "2DPb" : "",
        "2DPc" : "%(cur_val)d%% of health sector aid was provided through programme based approaches by the end of %(cur_year)s, %(diff_direction)s of %(diff_val)d%% from the %(base_year)s baseline. Target = %(target_val)s.",
        "3DP" : "%(cur_val)d%% of health sector funding was provided through multi-year commitments by the end of %(cur_year)s: %(diff_direction)s from %(base_val)d%% in %(base_year)s. Target = %(target_val)s.",
        "4DP" : "In %(cur_year)s, %(cur_val)d%% of health sector aid disbursements were released according to agreed schedules in annual or multi-year frameworks - %(diff_direction)s from %(base_val)d%% in %(base_year)s.",
        "5DPa" : "By end %(cur_year)s, %(cur_val)d%% of health sector aid used government partner country public financial management systems: %(diff_direction)s from %(base_val)d%% since %(base_year)s. Target = %(target_val)d%% of aid to be chanelled through partner country PFM systems.",
        "5DPb" : "By end %(cur_year)s, %(cur_val)d%% of health sector aid used country procurement systems in IHP+ partner countries: %(diff_direction)s from %(base_val)d%% in %(base_year)s. Target = %(target_val)d%% reduction in the %% of health sector aid to the public sector not useing partner country procurement systems.",
        "5DPc" : "",
        "6DP" : "Where they exist, national performance assessment frameworks are used to assess progress in %(cur_val)d%% of IHP+ countries: increased from %(base_val)d%% in %(base_year)s. Target = %(target_val)s%%.",
        "7DP" : "Participated in annual mutual assessments of progress in implementing health sector commitments & agreements (such as the IHP+ country compact and on aid effectiveness in the health sector) in all IHP+ countries. Target = %(target_val)d%%.",
        "8DP" : "",
    }
        
    targets = get_agency_targets(agency)
    indicators = calc_agency_indicators(agency)
    results = {}
    for indicator, ((base_val, base_year, cur_val, cur_year), comments) in indicators.items():
        target = targets[indicator]
        tick_func = criteria_funcs[target.tick_criterion_type]
        arrow_func = criteria_funcs[target.arrow_criterion_type]
        base_val = none_mul(base_val, 100)
        cur_val = none_mul(cur_val, 100)

        result = {
            "base_val" : base_val,
            "base_year" : base_year,
            "cur_val" : cur_val,
            "cur_year" : cur_year,
            "comments" : comments,
            "commentary" : "",
        }

        # create commentary
        if base_val != None and cur_val != None:
            result["diff_val"] = math.fabs(base_val - cur_val)
            result["diff_direction"] = "a decrease" if base_val - cur_val < 0 else "an increase"
            result["target_val"] = target.tick_criterion_value

            result["commentary"] = commentary_map[indicator] % result

        if tick_func(base_val, cur_val, target.tick_criterion_value):
            result["target"] = "tick"
        elif arrow_func(base_val, cur_val, target.arrow_criterion_value):
            result["target"] = "arrow"
        else:
            result["target"] = "cross"
        results[indicator] = result
    return results
