from indicators import calc_agency_indicators, calc_country_indicators, dp_indicators, g_indicators, calc_agency_country_indicators
from models import AgencyTargets, AgencyCountries, Submission, CountryTargets
import math

def criterion_absolute(base_val, cur_val, criterion_param):
    
    if cur_val == None: 
        raise MissingValueException() 
    if math.fabs(cur_val - criterion_param) < 0.000000001:
        return True
    return False

def criterion_relative_increase(base_val, cur_val, criterion_param):
    if cur_val == None or base_val == None: 
        raise MissingValueException() 

    if cur_val >= base_val * (1 + criterion_param / 100.0):
        return True
    return False

def criterion_relative_decrease(base_val, cur_val, criterion_param):
    if cur_val == None or base_val == None: 
        raise MissingValueException() 

    if cur_val <= base_val * (1 - criterion_param / 100.0):
        return True
    return False

def criterion_increase(base_val, cur_val, criterion_param):
    if cur_val == None or base_val == None: 
        raise MissingValueException() 

    if cur_val > base_val:
        return True
    return False

def criterion_decrease(base_val, cur_val, criterion_param):
    if cur_val == None or base_val == None: 
        raise MissingValueException()

    if cur_val < base_val:
        return True
    return False

def criterion_absolute_greater_than(base_val, cur_val, criterion_param):

    if cur_val == None: raise MissingValueException()
    if cur_val > criterion_param:
        return True
    return False

def criterion_absolute_less_than(base_val, cur_val, criterion_param):
    if cur_val == None: raise MissingValueException()
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
    if len(cur_val.strip()) != 2:
        raise MissingValueException()

    if cur_val.lower() == "yy":
        return True
    return False

class MissingValueException(Exception):
    pass

def criterion_first_yes(base_val, cur_val, criterion_param):
    if len(cur_val) == 0:
        raise MissingValueException()

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

    try:
        if tick_func(base_val, cur_val, target.tick_criterion_value):
            return "tick"
        elif arrow_func(base_val, cur_val, target.arrow_criterion_value):
            return "arrow"
        else:
            return "cross"
    except MissingValueException:
        return None

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
        "1DP" : "An IHP+ Country Compact or equivalent was signed in %(cur_val).2f%% of IHP+ countries where these exist, by the end of %(cur_year)s. Target = %(target_val).2f%%.",
        "2DPa" : "%(cur_val).2f%% of health sector aid was not reported on national health sector budgets by the end of %(cur_year)s - %(diff_direction)s from %(base_val).2f%% in 2006. Target = Halve the proportion of aid flows to the health sector not reported on government's budget(s) (with at least 85%% reported on budget).",
        "2DPb" :"%(cur_val).2f%% of capacity development support was provided through co-ordinated programmes in %(cur_year)s - %(diff_direction)s from %(base_val).2f%% in %(base_year)s. Target = %(target_val).2f%%",
        "2DPc" : "%(cur_val).2f%% of health sector aid was provided through programme based approaches by the end of %(cur_year)s, %(diff_direction)s from %(base_val).2f%% in the %(base_year)s baseline. Target = %(target_val).2f%%.",
        "3DP" : "%(cur_val).2f%% of health sector funding was provided through multi-year commitments by the end of %(cur_year)s: %(diff_direction)s from %(base_val).2f%% in %(base_year)s. Target = %(target_val).2f%%.",
        "4DP" : "In %(cur_year)s, %(cur_val).2f%% of health sector aid disbursements were not released according to agreed schedules in annual or multi-year frameworks - %(diff_direction)s from %(base_val).2f%% in %(base_year)s. Target = Halve the proportion of health sector aid not disbursed within the fiscal year for which it was scheduled.",
        "5DPa" : "By the end of %(cur_year)s, %(cur_val).2f%% of health sector aid did not use government partner country public financial management systems: %(diff_direction)s from %(base_val).2f%% since %(base_year)s. Target = One-third reduction in the %% of health sector aid to the public sector not using partner countries' procurement systems.",
        "5DPb" : "By end %(cur_year)s, %(cur_val).2f%% of health sector aid did not use country procurement systems in IHP+ partner countries: %(diff_direction)s from %(base_val).2f%% in %(base_year)s. Target = One-third reduction in the %% of health sector aid to the public sector not using partner countries' PFM systems.",
        "5DPc" : "There are no more than %(cur_val).2f parallel Project Implementation Units (PIUs) in any IHP+ country: %(diff_direction2)s from %(base_val).2f in %(base_year)s. Reduce by two-thirds the stock of parallel project implementation units (PIUs).",
        "6DP" : "Where they exist, national performance assessment frameworks are used to assess progress in %(cur_val).2f%% of IHP+ countries: increased from %(base_val).2f%% in %(base_year)s. Target = 100%%.",
        "7DP" : "In %(cur_year)s, participated in annual mutual assessments of progress in implementing health sector commitments & agreements in %(cur_val).2f%% IHP+ countries; %(diff_direction)s from %(base_val).2f%% in %(base_year)s.  Target: 100%%.",
        "8DP" : "By end %(cur_year)s, evidence exists in %(cur_val).2f%% of countries of support to civil society engagement in health sector policy processes; %(diff_direction)s from %(base_val).2f%% in %(base_year)s. Target = 100%%",
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
            "commentary" : None,
        }

        result["target"] = evaluate_indicator(target, base_val, cur_val)

        # create commentary
        if base_val != None and cur_val != None:
            result["diff_val"] = math.fabs(base_val - cur_val)
            if base_val - cur_val > 0:
                result["diff_direction"] = "a decrease" 
                result["diff_direction2"] = "down" 
            elif base_val - cur_val == 0:
                result["diff_direction"] = "no change"
                result["diff_direction2"] = "no change"
            else:
               result["diff_direction"] = "an increase"
               result["diff_direction2"] = "up"

            result["target_val"] = target.tick_criterion_value
            if target.tick_criterion_type == "Minimum x% Decrease relative to baseline":
                result["target_val"] = (1 - target.tick_criterion_value / 100.0) * base_val
            elif target.tick_criterion_type == "Minimum x% Increase relative to baseline":
                result["target_val"] = (1 + target.tick_criterion_value / 100.0) * base_val
            result["one_minus_base_val"] = 100 - result["base_val"]
            result["one_minus_cur_val"] = 100 - result["cur_val"]
            if result["target_val"] != None:
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

    commentary_text = {
        "1G": {
            "tick" : "An [space] was signed in [space] called [space]. Target = An IHP+ Compact or equivalent agreement in place",
            "arrow" : "There is evidence of a Compact or equivalent agreement under development. The aim is to have this in place by [space]",
            "cross" : "There are no current plans to develop a Compact or equivalent agreement",
        },
        "2Ga" : {
            "all" : "A National Health Sector Plan/Strategy is in place with current targets & budgets that have been jointly assessed.This one will have to be done manually",

        },
        "2Gb" : {
            "tick" : "There is curently a costed and evidence based HRH plan in place that is integrated with the national health plan. Target = A costed comprehensive national HRH plan that is integrated with the national health plan",
            "arrow" : """At the end of %(cur_year)s a costed and evidence based HRH plan was under development. Target = A costed comprehensive national HRH plan that is integrated with the national health plan

At the end of %(cur_year)s a costed and evidence based HRH plan was in place but not yet integrated with the national health plan. Target = A costed comprehensive national HRH plan that is integrated with the national health plan
""",
            "cross" : "At the end of %(cur_year)s there was no costed and evidence based HRH plan in place, or plans to develop one. Target = A costed comprehensive national HRH plan that is integrated with the national health plan",
        },
        "3G" : {
            "all" : "%(country_name)s allocated %(cur_val)s%% of its approved annual national budget to health in %(cur_year)s. Target = 15%% (or an alternative agreed published target)",
        },
        "4G" : {
            "all" : "In %(cur_year)s, %(cur_val)s%% of health sector funding was disbursed against the approved annual budget. Target = to halve the proportion of health sector funding not disbursed against the approved annual budget",
        },
        "5Ga" : {
            "all" : "In %(cur_year)s, %(country_name)s achieved a score of %(cur_val)s on the PFM/CPIA scale of performance. Target = Improvement of at least one measure (ie 0.5 points) on the PFM/CPIA scale of performance.  In %(cur_year)s, %(country_name)s achieved a score of %(cur_val)s on the PFM/CPIA scale of performance. Target = Improvement of at least one measure (ie 0.5 points) on the PFM/CPIA scale of performance."
        },
        "5Gb" : {
            "all" : "In %(cur_year)s, %(country_name)s achieved a score of %(cur_val)s on the four poin t scale used to assess performance in the the procurement sector. Target = Improvement of at least one measure on the four-point scale used to assess performance for this sector."
        },
        "6G" : {
            "tick" : "There is a transparent and monitorable performance assessment framework in place to assess progress against (a) the national development strategies relevant to health and (b) health sector programmes. Target = A transparent and monitorable performance assessment framework is in place to assess progress against (a) the national development strategies relevant to health and (b) health sector programmes.",
            "arrow" : "At the end of %(cur_year)s there was evidence that a transparent and monitorable performance assessment framework was under development to assess progress against (a) the national development  strategies relevant to health and (b) health sector programmes. Target = A transparent and monitorable performance assessment framework is in place to assess progress against (a) the national development strategies relevant to health and (b) health sector programmes.",
            "cross" : "At the end of %(cur_year)s there was no transparent and monitorable performance assessment framework in place and no plans to develop one were clear or being implemented. Target = A transparent and monitorable performance assessment framework is in place to assess progress against (a) the national development strategies relevant to health and (b) health sector programmes.",
        },
        "7G" : {
            "all" : "This one will have to be done manually. Target = Mutual assessments (such as a joint Annual Health Sector Review) are being made of progress implementing  commitments in the health sector, including on aid effectiveness."
        },
        "8G" : {
            "all" : "At the end of %(cur_year)s %(cur_val)s%% of seats in the Health Sector Coordination Mechanism (or equivalent body) were allocated to Civil Society representatives. Target = Evidence that Civil Society is actively represented in health sector policy processes - including Health Sector planning, coordination & review mechanisms."
        },
    }

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
            "country_name" : country,
        }

        result["target"] = evaluate_indicator(target, base_val, cur_val)
        if indicator in commentary_text:
            if "all" in commentary_text[indicator]:
                result["commentary"] = commentary_text[indicator]["all"]
            else:
                target_value = result["target"]
                if target_value == None:
                    result["commentary"] = "Missing Data"
                else:
                    result["commentary"] = commentary_text[indicator][target_value]
        
            result["commentary"] = result["commentary"] % result

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
