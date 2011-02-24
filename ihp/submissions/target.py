#-*- coding: utf-8 -*-
import numbers
from django.template import Context, Template
from django.utils.functional import memoize
from indicators import NA_STR
from indicators import calc_agency_indicators, calc_country_indicators, dp_indicators, g_indicators, calc_agency_country_indicators
from models import AgencyTargets, AgencyCountries, Submission, CountryTargets, Country8DPFix, GovScorecardRatings, DPScorecardRatings, Rating
from target_criteria import criteria_funcs, MissingValueException, CannotCalculateException
import math
from itertools import chain
from logging import debug
from django.utils.translation import ugettext_lazy as _
import translations

def get_agency_targets(agency, indicators):
    targets = {}
    agency_targets = AgencyTargets.objects.filter(agency=agency).select_related()
    none_targets = AgencyTargets.objects.filter(agency=None).select_related()

    for target in chain(none_targets, agency_targets):
        targets[target.indicator] = target
    return targets

def get_country_targets(country, indicators):
    targets = {}
    country_targets = CountryTargets.objects.filter(country=country)
    none_targets = CountryTargets.objects.filter(country=None)

    for target in chain(none_targets, country_targets):
        targets[target.indicator] = target
    return targets

def evaluate_indicator(target, base_val, cur_val):
    tick_func = criteria_funcs[target.tick_criterion_type]
    arrow_func = criteria_funcs[target.arrow_criterion_type]

    if cur_val not in [None, NA_STR]:
        if target.indicator in ["5DPa", "5DPb"]:
            if cur_val <= 20:
                return Rating.TICK
        elif target.indicator in ["2DPa"]:
            if cur_val <= 15:
                return Rating.TICK
        elif target.indicator in ["5DPc"]:
            if cur_val == 0:
                return Rating.TICK
        elif target.indicator in ["5Ga"]:
            if base_val not in [None, NA_STR]:
                if cur_val - base_val >= 0.5:
                    return Rating.TICK
        elif target.indicator in ["4G"]:
            if cur_val <= 20:
                return Rating.TICK

    try:
        if tick_func(base_val, cur_val, target.tick_criterion_value):
            return Rating.TICK
        elif arrow_func(base_val, cur_val, target.arrow_criterion_value):
            return Rating.ARROW
        else:
            return Rating.CROSS
    except MissingValueException:
        return Rating.QUESTION
    except CannotCalculateException:
        return Rating.NONE

commentary_map = {
    "1DP" : "An IHP+ Country Compact or equivalent has been signed by the agency in %(cur_val).0f%% of IHP+ countries where they exist. Target = 100%%.",
    "2DPa" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid was reported by the agency on national health sector budgets - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%. Target = 50%% reduction in aid not on budget (with > 85%% on budget).",
    "2DPb" :"In %(cur_year)s %(cur_val).0f%% of capacity development was provided by the agency through coordinated programmes - %(diff_direction)s from %(base_val).0f%%. Target = 50%%.",
    "2DPc" : "In %(cur_year)s %(cur_val).0f%% of health sector aid was provided by the agency through programme based approaches - %(diff_direction)s from %(base_val).0f%%. Target = 66%%.",
    "3DP" : "In %(cur_year)s %(cur_val).0f%% of health sector aid was provided by the agency through multi-year commitments - %(diff_direction)s from %(base_val).0f%%. Target = 90%%.",
    "4DP" : "In %(cur_year)s %(cur_val).0f%% of health sector aid disbursements provided by the agency were released according to agreed schedules - %(one_minus_diff_direction)s from %(base_val).0f%% in %(base_year)s. Target = 90%%.",
    "5DPa" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid provided by the agency used country procurement systems - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%. Target = 33%% reduction in aid not using procurement systems.",
    "5DPb" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid provided by the agency used national public financial management systems - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%. Target = 33%% reduction in aid not using PFM systems.",
    "5DPc" : "In %(cur_year)s the stock of parallel project implementation units (PIUs) used by the agency in the surveyed countries was %(cur_val)s - %(diff_direction)s from %(base_val)s. Target = 66%% reduction in stock of PIUs.",
    "6DP" : "In %(cur_year)s national performance assessment frameworks were routinely used by the agency to assess progress in %(cur_val).0f%% of IHP+ countries where they exist. Target = 100%%.",
    "7DP" : "In %(cur_year)s the agency participated in health sector mutual assessments of progress in %(cur_val).0f%% of IHP+ countries where they exist. Target = 100%%.",
    "8DP" : "In %(cur_year)s, evidence exists in %(cur_val).0f%% of IHP+ countries that the agency supported civil society engagement in health sector policy processes. Target = 100%%.",
}

default_text = "Insufficient data has been provided to enable a rating for this Standard Performance Measure."
na_text = "This Standard Performance Measure was deemed not applicable to %s."

def calc_agency_ratings(agency):
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

    def ratings_val(tmpl):
        def _func(indicator):
            h = indicator.replace("DP", "")
            d = ratings.__dict__
            return d.get(tmpl % h, None)
        return _func

    def round_to_zero(x):
        if type(x) == float and round(x, 0) == 0:
            return 0.0
        else:
            return x

    ratings_comments = ratings_val("er%s")
    ratings_target = ratings_val("r%s")

    targets = get_agency_targets(agency, dp_indicators)
    indicators = calc_agency_indicators(agency)
    ratings, _ = DPScorecardRatings.objects.get_or_create(agency=agency)
    results = {}

    for indicator in indicators:
        (base_val, base_year, cur_val, cur_year), comments = indicators[indicator]
        cur_val = round_to_zero(cur_val)
        base_val = round_to_zero(base_val)

        target = targets[indicator]

        result = {
            "base_val" : base_val,
            "base_year" : base_year,
            "cur_val" : cur_val,
            "cur_year" : cur_year,
            "comments" : comments,
            "commentary" : "",
            "agency_name" : agency.agency,
        }

        result["target"] = ratings_target(indicator) or evaluate_indicator(target, base_val, cur_val)
        result["target_val"] = target.tick_criterion_value

        if ratings_comments(indicator):
            result["commentary"] = ratings_comments(indicator)
        else:
            # create commentary
            if (base_val not in [None, NA_STR]) and (cur_val not in [None, NA_STR]):
                result["diff_val"] = math.fabs(base_val - cur_val)
                # This is really dirty but the text is currently formatted using
                # no decimal places and so this calculation should use the rounded
                # value
                diff = round(round(base_val) - round(cur_val))

                if diff > 0:
                    result["diff_direction"] = "a decrease" 
                    result["diff_direction2"] = "down" 
                    result["one_minus_diff_direction"] = "an increase" 
                elif diff == 0:
                    result["diff_direction"] = "no change"
                    result["diff_direction2"] = "no change"
                    result["one_minus_diff_direction"] = "no change" 
                else:
                   result["diff_direction"] = "an increase"
                   result["diff_direction2"] = "up"
                   result["one_minus_diff_direction"] = "a decrease" 

                if result["base_val"] > 0:
                    result["perc_change"] = (result["cur_val"] - result["base_val"]) / float(result["base_val"]) * 100
                    result["abs_perc_change"] = math.fabs(result["perc_change"])
                else:
                    result["perc_change"] = 0
                    result["abs_perc_change"] = 0

                result["one_minus_base_val"] = 100 - result["base_val"]
                result["one_minus_cur_val"] = 100 - result["cur_val"]
        
            try:
                template = commentary_map[indicator]
                if type(template) == Template:
                    result["commentary"] = template.render(Context(result))
                else:
                    result["commentary"] = template % result
            except:
                pass

            if result["target"] == Rating.NONE:
            #if NA_STR in [base_val, cur_val]:
                result["commentary"] = na_text % agency.agency
            elif result["commentary"] == "":
                result["commentary"] = default_text
            result["commentary"] += u"∆"

        results[indicator] = result

    return results

def calc_country_ratings(country, language="en"):
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

    translation = translations.get_translation(language)
    gov_commentary_text = translation.gov_commentary_text

    rating_question_text = translation.rating_question_text
    rating_none_text = translation.rating_none_text % country.country

    targets = get_country_targets(country, g_indicators)
    indicators = calc_country_indicators(country)
    results = {}
    ratings, _ = GovScorecardRatings.objects.get_or_create(country=country)

    def ratings_val(tmpl):
        def _func(indicator):
            h = indicator.replace("G", "").replace("Q", "")
            d = ratings.__dict__
            return d.get(tmpl % h, None)
        return _func

    ratings_comments = ratings_val("er%s")
    ratings_target = ratings_val("r%s")

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

        result["one_minus_base_val"] = base_val
        if isinstance(base_val, numbers.Real):
            result["one_minus_base_val"] = 100 - base_val

        result["one_minus_cur_val"] = cur_val
        if isinstance(cur_val, numbers.Real):
            result["one_minus_cur_val"] = 100 - cur_val
        
        result["target"] = ratings_target(indicator) or evaluate_indicator(target, base_val, cur_val)
        if ratings_comments(indicator):
            result["commentary"] = ratings_comments(indicator)
        else:
            if indicator in gov_commentary_text:
                target_value = result["target"]
                if target_value == Rating.QUESTION:
                    commentary = rating_question_text
                elif target_value == Rating.NONE:
                    commentary = rating_none_text
                elif target_value == None:
                    raise Exception("This shouldn't really be happening")
                    commentary = "Missing Data"
                elif "all" in gov_commentary_text[indicator]:
                    commentary = gov_commentary_text[indicator]["all"]
                else:
                    commentary = gov_commentary_text[indicator][target_value]
                commentary += u"∆"
                
                try:
                    result["commentary"] = commentary % result
                except TypeError, e:
                    result["commentary"] = ["This text couldn't be generated, possibly because the rating was overriden. Please override the text appropriately as well"]

        results[indicator] = result
    return results

def country_agency_indicator_ratings(country, agency):
    """
    Evaluate ratings for a country-agency per indicator
    """
    indicators = {}
    targets = get_agency_targets(agency, dp_indicators)
    country_indicators = calc_agency_country_indicators(agency, country)

    for indicator in country_indicators:
        v = country_indicators[indicator]
        debug("extracting %s from %s" % (indicator, str(country_indicators)))
        values, comments = v
        (base_val, base_year, cur_val, cur_year) = values
        # TODO this is a hack - it might be better to extract this
        # logic out of here
        result = None
        if indicator in ["1DP", "6DP", "7DP"] and cur_val != NA_STR:
            if cur_val > 0: 
                result = Rating.TICK
            elif base_val == None and cur_val == None:
                result = Rating.QUESTION
            elif base_val in [None, NA_STR]:
                result = Rating.CROSS
        elif indicator == "8DP":
            try:
                fix = Country8DPFix.objects.get(agency=agency, country=country)
                result = fix.latest_progress
            except Country8DPFix.DoesNotExist:
                result = Rating.QUESTION

        if result == None:
            target = targets[indicator]
            result = evaluate_indicator(target, base_val, cur_val)
        indicators[indicator] = result
    return indicators

def country_agency_progress(country, agency):
    """
    Returns True is an agency is making progress in a particular country
    Progress is defined as (# ticks + # arrows) / # ratings >= 0.5
    """
    is_tick = lambda x : x == Rating.TICK or x == Rating.ARROW
    ratings = country_agency_indicator_ratings(country, agency)
    ratings = dict([(indicator, rating) for (indicator, rating) in ratings.items() if rating  != Rating.NONE])
    ticks = filter(is_tick, ratings.values())

    if len(ratings) == 0: 
        return False
    return len(ticks) / float(len(ratings)) >= 0.5

def get_country_progress(agency):
    """
    Get the list of countries in which the agency is making progress and not making progress
    """
    np = []
    p = []
    np_dict = {}
    p_dict = {}
    for country in AgencyCountries.objects.get_agency_countries(agency):
        if Submission.objects.filter(agency=agency, country=country).count() == 0:
            np.append(country)
        else:
            if country_agency_progress(country, agency):
                p.append(country)
            else:
                np.append(country)
    for i, country in enumerate(sorted(p, key=lambda x : x.country)):
        p_dict[i] = country
    for i, country in enumerate(sorted(np, key=lambda x : x.country)):
        np_dict[i] = country
        
    return np_dict, p_dict

def get_agency_progress(country):
    """
    Get the list of agencies which are making progress and which are not making progress
    """
    np = []
    p = []
    np_dict = {}
    p_dict = {}
    
    for agency in AgencyCountries.objects.get_country_agencies(country):
        if Submission.objects.filter(agency=agency, country=country).count() == 0:
            np.append(agency)
        else:
            if country_agency_progress(country, agency):
                p.append(agency)
            else:
                np.append(agency)
    for i, agency in enumerate(sorted(p, key=lambda x : x.agency)):
        p_dict[i] = agency
    for i, agency in enumerate(sorted(np, key=lambda x : x.agency)):
        np_dict[i] = agency
        
    return np_dict, p_dict
