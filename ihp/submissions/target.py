from indicators import calc_agency_indicators, indicators
from models import Targets

def criterion_absolute(base_val, cur_val, criterion_param):
    
    if cur_val * 100 - criterion_param < 0.000000001:
        return True
    return False

def criterion_relative_increase(base_val, cur_val, criterion_param):
    if cur_val >= base_val * (1 + criterion_param / 100.0):
        return True
    return False

def criterion_relative_decrease(base_val, cur_val, criterion_param):
    if cur_val <= base_val * (1 - criterion_param / 100.0):
        return True
    return False

def criterion_increase(base_val, cur_val, criterion_param):
    if cur_val > base_val:
        return True
    return False

def criterion_decrease(base_val, cur_val, criterion_param):
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
            target = Targets.objects.get(agency="Default", indicator=indicator)
        targets[indicator] = target
    return targets

def calc_agency_targets(agency):
    targets = get_agency_targets(agency)
    indicators = calc_agency_indicators(agency)
    results = {}
    for indicator, ((base_val, cur_val), comments) in indicators.items():
        target = targets[indicator]
        tick_func = criteria_funcs[target.tick_criterion_type]
        arrow_func = criteria_funcs[target.arrow_criterion_type]

        result = {
            "base_val" : base_val,
            "cur_val" : cur_val,
            "comments" : comments,
        }
        if tick_func(base_val, cur_val, target.tick_criterion_value):
            result["target"] = "tick"
        elif arrow_func(base_val, cur_val, target.arrow_criterion_value):
            result["target"] = "arrow"
        else:
            result["target"] = "cross"
        results[indicator] = result
    return results
