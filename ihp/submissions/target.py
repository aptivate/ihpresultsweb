#-*- coding: utf-8 -*-
import numbers
from django.template import Context, Template
from django.utils.functional import memoize
from indicators import NA_STR
from indicators import calc_agency_indicators, calc_country_indicators, dp_indicators, g_indicators, calc_agency_country_indicators
from models import AgencyTargets, AgencyCountries, Submission, CountryTargets, Country8DPFix, GovScorecardRatings, CountryLanguage, DPScorecardRatings, Rating
from target_criteria import criteria_funcs, MissingValueException, CannotCalculateException
import math
from itertools import chain

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

    commentary_map = {
        "1DP" : "An IHP+ Country Compact or equivalent has been signed in %(cur_val).0f%% of IHP+ countries where they exist.",
        "2DPa" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid was reported on national health sector budgets - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%.",
        "2DPb" :"In %(cur_year)s %(cur_val).0f%% of capacity development was provided through coordinated programmes - %(diff_direction)s from %(base_val).0f%%.",
        "2DPc" : "In %(cur_year)s %(cur_val).0f%% of health sector aid was provided through programme based approaches - %(diff_direction)s from %(base_val).0f%%.",
        "3DP" : "In %(cur_year)s %(cur_val).0f%% of health sector aid was provided through multi-year commitments - %(diff_direction)s from %(base_val).0f%%.",
        "4DP" : "In %(cur_year)s %(cur_val).0f%% of actual health sector spending was planned for that year - %(diff_direction)s from %(base_val).0f%%.",
        "5DPa" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid used country procurement systems - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%.",
        "5DPb" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid used national public financial management systems - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%.",
        "5DPc" : "In %(cur_year)s the stock of parallel project implementation units (PIUs) in the surveyed countries was %(cur_val)s - %(diff_direction)s from %(base_val)s.",
        "6DP" : "In %(cur_year)s national performance assessment frameworks were used to assess progress in %(cur_val).0f%% of IHP+ countries - %(diff_direction)s from %(base_val).0f%%",
        "7DP" : "In %(cur_year)s %(agency_name)s participated in health sector annual mutual assessments of progress in %(cur_val).0f%% IHP+ countries - %(diff_direction)s from %(base_val).0f%%.",
        "8DP" : "In %(cur_year)s, evidence exists in %(cur_val).0f%% of IHP+ countries of support to civil society engagement in health sector policy processes.",
    }

    default_text = "Insufficient data has been provided to enable a rating for this Standard Performance Measure."
    na_text = "This Standard Performance Measure was deemed not applicable to %s." % agency.agency

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

            if NA_STR in [base_val, cur_val]:
                result["commentary"] = na_text
            elif result["commentary"] == "":
                result["commentary"] = default_text
            result["commentary"] += u"∆"

        results[indicator] = result

    return results

gov_commentary_text_en = {
    "1G": {
        Rating.TICK : "An [space] was signed in [space] called [space].",
        Rating.ARROW : "There is evidence of a Compact or equivalent agreement under development. The aim is to have this in place by [space].",
        Rating.CROSS : "There are no current plans to develop a Compact or equivalent agreement.",
    },
    "2Ga" : {
        Rating.TICK : "A National Health Sector Plan/Strategy is in place with current targets & budgets that have been jointly assessed.",
        Rating.ARROW : "National Health Sector Plans/Strategy in place with current targets & budgets with evidence of plans for joint assessment.",
        Rating.CROSS : "National Health Sector Plans/Strategy in place with no plans for joint assessment. Target = National Health Sector Plans/Strategy in place with current targets & budgets that have been jointly assessed.",

    },
    "2Gb" : {
        Rating.TICK : "There is currently a costed and evidence based HRH plan in place that is integrated with the national health plan.",
        Rating.ARROW : """At the end of %(cur_year)s a costed and evidence based HRH plan was under development. 

At the end of %(cur_year)s a costed and evidence based HRH plan was in place but not yet integrated with the national health plan. """,
        Rating.CROSS : "At the end of %(cur_year)s there was no costed and evidence based HRH plan in place, or plans to develop one. ",
    },
    "3G" : {
        "all" : "In %(cur_year)s %(country_name)s allocated %(cur_val).1f%% of its approved annual national budget to health.",
    },
    "4G" : {
        "all" : "In %(cur_year)s, %(one_minus_cur_val).0f%% of health sector funding was disbursed against the approved annual budget.",
    },
    "5Ga" : {
        "all" : "In %(cur_year)s, %(country_name)s achieved a score of %(cur_val).1f on the PFM/CPIA scale of performance."
    },
    "5Gb" : {
        "all" : "In %(cur_year)s, %(country_name)s achieved a score of %(cur_val).0f on the four point scale used to assess performance in the the procurement sector."
    },
    "6G" : {
        Rating.TICK : "In %(cur_year)s there was a transparent and monitorable performance assessment framework in place to assess progress against (a) the national development strategies relevant to health and (b) health sector programmes.",
        Rating.ARROW : "At the end of %(cur_year)s there was evidence that a transparent and monitorable performance assessment framework was under development to assess progress against (a) the national development  strategies relevant to health and (b) health sector programmes.",
        Rating.CROSS : "At the end of %(cur_year)s there was no transparent and monitorable performance assessment framework in place and no plans to develop one were clear or being implemented.",
    },
    "7G" : {
        Rating.TICK : "Mutual assessments are being made of progress implementing commitments in the health sector, including on aid effectiveness.",
        Rating.ARROW : "Mutual assessments are being made of progress implementing commitments in the health sector, but not on aid effectiveness.",
        Rating.CROSS : "Mutual assessments are not being made of progress implementing commitments in the health sector.",
    },
    "8G" : {
        "all" : "In %(cur_year)s %(cur_val).0f% of seats in the Health Sector Coordination Mechanism (or equivalent body) were allocated to Civil Society representatives."
    },
}

gov_commentary_text_fr = {
    "1G": {
        Rating.TICK : u"Un [space] a été signé en [space] qui se nomme [space].",
        Rating.ARROW : u"Certaines données indiquent qu’un accord ou une entente équivalente est en cours d’élaboration. L’objectif poursuivi est la mise en place de cet accord ou de cette entente avant le [space].",
        Rating.CROSS : u"Il n’y a actuellement aucun plan visant à élaborer un accord ou une entente équivalente.",
    },
    "2Ga" : {
        Rating.TICK : u"Un plan et une stratégie nationaux sectoriels de santé ont été mis en place à l’aide des objectifs et des budgets actuels qui ont été évalués conjointement.",
        Rating.ARROW : u"Mise en place de plans et d'une stratégie nationaux sectoriels de santé à l’aide des objectifs et des budgets actuels qui ont été évalués conjointement.",
        Rating.CROSS : u"Mise en place de plans et d’une stratégie nationaux sectoriels de santé sans plan d’évaluation conjointe.",

    },
    "2Gb" : {
        Rating.TICK : u"Un plan relatif aux HRH chiffré et fondé sur des preuves qui est intégré au plan de santé national a été mis en place.",
        Rating.ARROW : u"""
À la fin de %(cur_year)s, un plan relatif aux HRH chiffré et fondé sur des preuves était en cours d’élaboration. 

À la fin de %(cur_year)s, un plan relatif aux HRH chiffré et fondé sur des preuves avait été mis en place, mais n’était pas encore intégré au plan de santé national. 
""",
        Rating.CROSS : u"À la fin de %(cur_year)s, aucun plan chiffré et fondé sur des preuves relatif aux HRH n’avait été mis en place ni aucun plan visant à en élaborer un.",
    },
    "3G" : {
        "all" : u"En %(cur_year)s, %(country_name)s a alloué %(cur_val).1f%% de son budget annuel ayant été approuvé pour le secteur de la santé.",
    },
    "4G" : {
        "all" : u"En %(cur_year)s, %(one_minus_cur_val).0f%% du financement alloué au secteur de la santé a été décaissé en fonction du budget annuel ayant été autorisé.",
    },
    "5Ga" : {
        "all" : u"En %(cur_year)s, %(country_name)s a obtenu un résultat de %(cur_val) sur l'échelle de performance GFP/EPIN."
    },
    "5Gb" : {
        "all" : u"En %(cur_year)s, %(country_name)s a obtenu un résultat de %(cur_val).0f sur l’échelle d’évaluation à quatre points utilisée pour évaluer la performance du secteur de l’approvisionnement. "
    },
    "6G" : {
        Rating.TICK : u"En %(cur_year)s, un cadre d’évaluation de la performance transparent et contrôlable a été mis en place pour évaluer les progrès accomplis par rapport aux a) stratégies de développement national relatives à la santé et aux b) programmes sectoriels de santé.",
        Rating.ARROW : u"À la fin de %(cur_year)s, certaines données indiquaient qu’un cadre d’évaluation de la performance transparent et contrôlable était en cours d’élaboration pour évaluer les progrès accomplis par rapport aux a) stratégies de développement national relatives à la santé et aux b) programmes sectoriels de santé.",
        Rating.CROSS : u"À la fin de %(cur_year)s, aucun cadre d'évaluation de la performance transparent et contrôlable n’avait été mis en place et aucun plan visant à en développer un n’était clair ou sur le point d’être mis en œuvre.",
    },
    "7G" : {
        Rating.TICK : u"Des évaluations conjointes sont faites des progrès accomplis en ce qui concerne la mise en œuvre d’engagements dans le secteur de la santé, notamment en matière d’efficacité de l’aide.",
        Rating.ARROW : u"Des évaluations conjointes sont faites des progrès accomplis en ce qui concerne la mise en œuvre d’engagements dans le secteur de la santé, mais pas en matière d’efficacité de l’aide.",
        Rating.CROSS : u"Des évaluations conjointes sont faites des progrès accomplis en ce qui concerne la mise en œuvre d’engagements dans le secteur de la santé.",
    },
    "8G" : {
        "all" : u"En %(cur_year)s, %(cur_val).0f%% des voix dans les mécanismes nationaux de coordination du secteur de la santé (ou un organe équivalent) ont été allouées aux représentants de la société civile."
    },
}

def get_country_commentary_text(country):
    try:
        cl = CountryLanguage.objects.get(country=country)
        if cl.language == "French":
            return gov_commentary_text_fr
    except CountryLanguage.DoesNotExist:
        pass
    return gov_commentary_text_en

def calc_country_ratings(country):
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

    
    gov_commentary_text = get_country_commentary_text(country)

    rating_question_text = "Insufficient data has been provided to enable a rating for this Standard Performance Measure."
    rating_none_text = "This Standard Performance Measure was deemed not applicable to %s." % country.country

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
        (base_val, base_year, cur_val, cur_year), comments = country_indicators[indicator]
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
                if fix.latest_progress:
                    result = Rating.TICK
                else:
                    result = Rating.CROSS
            except Country8DPFix.DoesNotExist:
                result = Rating.CROSS

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
