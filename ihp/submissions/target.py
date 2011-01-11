#-*- coding: utf-8 -*-
from django.template import Context, Template
from django.utils.functional import memoize
from indicators import NA_STR
from indicators import calc_agency_indicators, calc_country_indicators, dp_indicators, g_indicators, calc_agency_country_indicators
from models import AgencyTargets, AgencyCountries, Submission, CountryTargets, Country8DPFix, GovScorecardRatings, CountryLanguage
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

    if cur_val == NA_STR or base_val == NA_STR:
        return "none"

    if target.indicator in ["4DP", "5DPa", "5DPb"]:
        if cur_val <= 20:
            return "tick" 
    elif target.indicator in ["2DPa"]:
        if cur_val <= 15:
            return "tick" 

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
        "1DP" : "An IHP+ Country Compact or equivalent has been signed in %(cur_val).0f%% of IHP+ countries where they exist.",
        "2DPa" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid was reported on national health sector budgets - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%.",
        "2DPb" :"In %(cur_year)s %(cur_val).0f%% of capacity development was provided through coordinated programmes - %(diff_direction)s from %(base_val).0f%%.",
        "2DPc" : "In %(cur_year)s %(cur_val).0f%% of health sector aid was provided through programme based approaches - %(diff_direction)s from %(base_val).0f%%.",
        "3DP" : "In %(cur_year)s %(cur_val).0f%% of health sector aid was provided through multi-year commitments - %(diff_direction)s from %(base_val).0f%%.",
        "4DP" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid disbursements were released according to agreed schedules - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%% in %(base_year)s.",
        "5DPa" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid used country procurement systems - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%.",
        "5DPb" : "In %(cur_year)s %(one_minus_cur_val).0f%% of health sector aid used national public financial management systems - %(one_minus_diff_direction)s from %(one_minus_base_val).0f%%.",
        "5DPc" : "In %(cur_year)s the stock of parallel project implementation units (PIUs) in the surveyed countries was %(cur_val)s - %(diff_direction)s from %(base_val)s.",
        "6DP" : "In %(cur_year)s national performance assessment frameworks were used to assess progress in %(cur_val).0f%% of IHP+ countries - %(diff_direction)s from %(base_val).0f%%",
        "7DP" : "In %(cur_year)s %(agency_name)s participated in health sector annual mutual assessments of progress in %(cur_val).0f%% IHP+ countries - %(diff_direction)s from %(base_val).0f%%.",
        "8DP" : "In %(cur_year)s, evidence exists in %(cur_val).0f%% of IHP+ countries of support to civil society engagement in health sector policy processes.",
    }

    target_map = {
        "1DP" : "Target = 100%%.",
        "2DPa" : "Target = Halve the %% of aid flows not reported on budget (with at least 85%% reported on budget).",
        "2DPb" :"Target = 50%%",
        "2DPc" : "Target = 66%%",
        "3DP" : "Target = 90%%",
        "4DP" : "Target = Halve the %% of health sector aid not disbursed within the calendar year for which it was scheduled.",
        "5DPa" : "Target = One third reduction in the %% of health sector aid to the public sector not using national procurement systems.",
        "5DPb" : "Target = One third reduction in the %% of health sector aid to the public sector not using national PFM systems.",
        "5DPc" : "Target = two-third reduction in the stock of parallel PIUs.",
        "6DP" : "Target = 100%%.",
        "7DP" : "Target: 100%%.",
        "8DP" : "Target = 100%%",
    }

    default_text = "Insufficient data has been provided to enable a rating for this Standard Performance Measure."
    na_text = "This Standard Performance Measure was deemed not applicable to %s." % agency.agency
        
    targets = get_agency_targets(agency, dp_indicators)
    indicators = calc_agency_indicators(agency)
    results = {}
    for indicator in indicators:

        (base_val, base_year, cur_val, cur_year), comments = indicators[indicator]

        if type(cur_val) == float and round(cur_val, 0) == 0:
            cur_val = 0.0

        if type(base_val) == float and round(base_val, 0) == 0:
            base_val = 0.0

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

        result["target"] = evaluate_indicator(target, base_val, cur_val)
        result["target_val"] = target.tick_criterion_value

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

        result["commentary"] = (result["commentary"] + " " + target_map[indicator] % result).strip()
        results[indicator] = result

    return results

gov_commentary_text_en = {
    "1G": {
        "tick" : "An [space] was signed in [space] called [space]. Target = An IHP+ Compact or equivalent agreement in place",
        "arrow" : "There is evidence of a Compact or equivalent agreement under development. The aim is to have this in place by [space]. Target = An IHP+ Compact or equivalent agreement in place.",
        "cross" : "There are no current plans to develop a Compact or equivalent agreement. Target = An IHP+ Compact or equivalent agreement in place.",
    },
    "2Ga" : {
        "tick" : "A National Health Sector Plan/Strategy is in place with current targets & budgets that have been jointly assessed. Target = National Health Sector Plans/Strategy in place with current targets & budgets that have been jointly assessed.",
        "arrow" : "National Health Sector Plans/Strategy in place with current targets & budgets with evidence of plans for joint assessment. Target = National Health Sector Plans/Strategy in place with current targets & budgets that have been jointly assessed.",
        "cross" : "National Health Sector Plans/Strategy in place with no plans for joint assessment. Target = National Health Sector Plans/Strategy in place with current targets & budgets that have been jointly assessed.",

    },
    "2Gb" : {
        "tick" : "There is currently a costed and evidence based HRH plan in place that is integrated with the national health plan. Target = A costed comprehensive national HRH plan that is integrated with the national health plan",
        "arrow" : """At the end of %(cur_year)s a costed and evidence based HRH plan was under development. Target = A costed comprehensive national HRH plan that is integrated with the national health plan

At the end of %(cur_year)s a costed and evidence based HRH plan was in place but not yet integrated with the national health plan. Target = A costed comprehensive national HRH plan that is integrated with the national health plan.
""",
        "cross" : "At the end of %(cur_year)s there was no costed and evidence based HRH plan in place, or plans to develop one. Target = A costed comprehensive national HRH plan that is integrated with the national health plan",
    },
    "3G" : {
        "all" : "In %(cur_year)s %(country_name)s allocated %(cur_val).0f%% of its approved annual national budget to health. Target = 15%% (or an alternative agreed published target)",
    },
    "4G" : {
        "all" : "In %(cur_year)s, %(cur_val).0f%% of health sector funding was disbursed against the approved annual budget. Target = to halve the proportion of health sector funding not disbursed against the approved annual budget",
    },
    "5Ga" : {
        "all" : "In %(cur_year)s, %(country_name)s achieved a score of %(cur_val).1f on the PFM/CPIA scale of performance. Target = Improvement of at least one measure (ie 0.5 points) on the PFM/CPIA scale of performance."
    },
    "5Gb" : {
        "all" : "In %(cur_year)s, %(country_name)s achieved a score of %(cur_val).0f on the four point scale used to assess performance in the the procurement sector. Target = Improvement of at least one measure on the four-point scale used to assess performance for this sector."
    },
    "6G" : {
        "tick" : "In %(cur_year)s there was a transparent and monitorable performance assessment framework in place to assess progress against (a) the national development strategies relevant to health and (b) health sector programmes. Target = A transparent and monitorable performance assessment framework is in place to assess progress against (a) the national development strategies relevant to health and (b) health sector programmes.",
        "arrow" : "At the end of %(cur_year)s there was evidence that a transparent and monitorable performance assessment framework was under development to assess progress against (a) the national development  strategies relevant to health and (b) health sector programmes. Target = A transparent and monitorable performance assessment framework is in place to assess progress against (a) the national development strategies relevant to health and (b) health sector programmes.",
        "cross" : "At the end of %(cur_year)s there was no transparent and monitorable performance assessment framework in place and no plans to develop one were clear or being implemented. Target = A transparent and monitorable performance assessment framework is in place to assess progress against (a) the national development strategies relevant to health and (b) health sector programmes.",
    },
    "7G" : {
        "tick" : "Mutual assessments are being made of progress implementing commitments in the health sector, including on aid effectiveness. Target = Mutual assessments (such as a joint Annual Health Sector Review) are being made of progress implementing  commitments in the health sector, including on aid effectiveness.",
        "arrow" : "Mutual assessments are being made of progress implementing commitments in the health sector, but not on aid effectiveness. Target = Mutual assessments (such as a joint Annual Health Sector Review) are being made of progress implementing  commitments in the health sector, including on aid effectiveness.",
        "cross" : "Mutual assessments are not being made of progress implementing commitments in the health sector. Target = Mutual assessments (such as a joint Annual Health Sector Review) are being made of progress implementing  commitments in the health sector, including on aid effectiveness. ",
    },
    "8G" : {
        "all" : "In %(cur_year)s %(cur_val).0f% of seats in the Health Sector Coordination Mechanism (or equivalent body) were allocated to Civil Society representatives. Target = Evidence that Civil Society is actively represented in health sector policy processes, including Health Sector planning, coordination & review mechanisms. "
    },
}

gov_commentary_text_fr = {
    "1G": {
        "tick" : u"Un [space] a été signé en [space] qui se nomme [space]. Objectif-cible = Mise en place d’un accord IHP+ ou d’une entente mutuelle équivalente.",
        "arrow" : u"Certaines données indiquent qu’un accord ou une entente équivalente est en cours d’élaboration. L’objectif poursuivi est la mise en place de cet accord ou de cette entente avant le [space].Objectif-cible = Mise en place d’un accord IHP+ ou d’une entente mutuelle équivalente.",
        "cross" : u"Il n’y a actuellement aucun plan visant à élaborer un accord ou une entente équivalente. Objectif-cible = Mise en place d’un accord IHP+ ou d’une entente mutuelle équivalente.",
    },
    "2Ga" : {
        "tick" : u"Un plan et une stratégie nationaux sectoriels de santé ont été mis en place à l’aide des objectifs et des budgets actuels qui ont été évalués conjointement. Objectif-cible = Mise en place d’un plan et d’une stratégie nationaux sectoriels de santé à l’aide des objectifs et des budgets actuels qui ont été évalués conjointement.",
        "arrow" : u"Mise en place de plans et d'une stratégie nationaux sectoriels de santé à l’aide des objectifs et des budgets actuels qui ont été évalués conjointement. Objectif-cible = Mise en place de plans et d’une stratégie nationaux sectoriels de santé à l’aide des objectifs et des budgets actuels qui ont été évalués conjointement.",
        "cross" : u"Mise en place de plans et d’une stratégie nationaux sectoriels de santé sans plan d’évaluation conjointe. Objectif-cible = Mise en place de plans et d’une stratégie nationaux sectoriels de santé à l’aide des objectifs et des budgets actuels qui ont été évalués conjointement.",

    },
    "2Gb" : {
        "tick" : u"Un plan relatif aux HRH chiffré et fondé sur des preuves qui est intégré au plan de santé national a été mis en place. Objectif-cible = Intégration d’un plan national chiffré et complet relatif aux HRH au plan de santé national.",
        "arrow" : u"""
À la fin de %(cur_year)s, un plan relatif aux HRH chiffré et fondé sur des preuves était en cours d’élaboration. Objectif-cible = Intégration d’un plan national chiffré et complet relatif aux HRH au plan de santé national.

À la fin de %(cur_year)s, un plan relatif aux HRH chiffré et fondé sur des preuves avait été mis en place, mais n’était pas encore intégré au plan de santé national. Objectif-cible = Intégration d’un plan national chiffré et complet relatif aux HRH au plan de santé national.
""",
        "cross" : u"À la fin de %(cur_year)s, aucun plan chiffré et fondé sur des preuves relatif aux HRH n’avait été mis en place ni aucun plan visant à en élaborer un. Objectif-cible = Intégration d’un plan national chiffré et complet relatif aux HRH au plan de santé national.",
    },
    "3G" : {
        "all" : u"En %(cur_year)s, %(country_name)s a alloué %(cur_val).0f%% de son budget annuel ayant été approuvé pour le secteur de la santé. Objectif-cible = 15 % (ou autres objectifs-cibles convenus ayant été publiés).",
    },
    "4G" : {
        "all" : u"En %(cur_year)s, %(cur_val).0f%% du financement alloué au secteur de la santé a été décaissé en fonction du budget annuel ayant été autorisé. Objectif-cible = Réduire de moitié de la proportion du financement alloué au secteur de la santé qui n’a pas été décaissée en fonction du budget annuel ayant été autorisé.",
    },
    "5Ga" : {
        "all" : u"En %(cur_year)s, %(country_name)s a obtenu un résultat de %(cur_val) sur l'échelle de performance PFM/CPIA. Objectif-cible = Augmentation d’au moins une mesure (0,5 point) sur l’échelle de performance PFM/CPIA."
    },
    "5Gb" : {
        "all" : u"En %(cur_year)s, %(country_name)s a obtenu un résultat de %(cur_val).0f sur l’échelle d’évaluation à quatre points utilisée pour évaluer la performance du secteur de l’approvisionnement. Objectif-cible = Augmentation d’au moins une mesure sur l’échelle d’évaluation à quatre points qui est utilisée pour évaluer la performance de ce secteur."
    },
    "6G" : {
        "tick" : u"En %(cur_year)s, un cadre d’évaluation de la performance transparent et contrôlable a été mis en place pour évaluer les progrès accomplis par rapport aux a) stratégies de développement national relatives à la santé et aux b) programmes sectoriels de santé. Objectif-cible = Mise en place d’un cadre d’évaluation de la performance transparent et contrôlable pour évaluer les progrès accomplis par rapport aux a) stratégies de développement national relatives à la santé et aux b) programmes sectoriels de santé.",
        "arrow" : u"À la fin de %(cur_year)s, certaines données indiquaient qu’un cadre d’évaluation de la performance transparent et contrôlable était en cours d’élaboration pour évaluer les progrès accomplis par rapport aux a) stratégies de développement national relatives à la santé et aux b) programmes sectoriels de santé. Objectif-cible = Mettre en place un cadre d’évaluation de la performance transparent et contrôlable pour évaluer les progrès accomplis par rapport aux a) stratégies de développement national relatives à la santé et aux b) programmes sectoriels de santé.",
        "cross" : u"À la fin de %(cur_year)s, aucun cadre d'évaluation de la performance transparent et contrôlable n’avait été mis en place et aucun plan visant à en développer un n’était clair ou sur le point d’être mis en œuvre. Objectif-cible = Mettre en place un cadre d’évaluation de la performance transparent et contrôlable pour évaluer les progrès accomplis par rapport aux a) stratégies de développement national relatives à la santé et aux b) programmes sectoriels de santé.",
    },
    "7G" : {
        "tick" : u"Des évaluations conjointes sont faites des progrès accomplis en ce qui concerne la mise en œuvre d’engagements dans le secteur de la santé, notamment en matière d’efficacité de l’aide. Objectif-cible = Effectuer des évaluations conjointes telles que les examens sectoriels annuels conjoints en matière de santé sur les progrès accomplis en ce qui concerne la mise en œuvre d'engagements dans le secteur de la santé, notamment en matière d’efficacité de l'aide.",
        "arrow" : u"Des évaluations conjointes sont faites des progrès accomplis en ce qui concerne la mise en œuvre d’engagements dans le secteur de la santé, mais pas en matière d’efficacité de l’aide. Objectif-cible = Effectuer des évaluations conjointes telles que les examens sectoriels annuels conjoints en matière de santé sur les progrès accomplis en ce qui concerne la mise en œuvre d'engagements dans le secteur de la santé, notamment en matière d’efficacité de l'aide.",
        "cross" : u"Des évaluations conjointes sont faites des progrès accomplis en ce qui concerne la mise en œuvre d’engagements dans le secteur de la santé. Objectif-cible = Effectuer des évaluations conjointes telles que les examens sectoriels annuels conjoints en matière de santé sur les progrès accomplis en ce qui concerne la mise en œuvre d'engagements dans le secteur de la santé, notamment en matière d’efficacité de l'aide.",
    },
    "8G" : {
        "all" : u"En %(cur_year)s, %(cur_val).0f%% des voix dans les mécanismes nationaux de coordination du secteur de la santé (ou un organe équivalent) ont été allouées aux représentants de la société civile. Objectif-cible = Prouver que la société civile est représentée activement dans les processus relatifs aux politiques dans le secteur de la santé, notamment la planification, la coordination et les mécanismes d’examen dans le secteur de la santé."
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

    
    gov_commentary_text = get_country_commentary_text(country)

    rating_question_text = "[Insert some standard text here for question ratings]"
    rating_none_text = "[Insert some standard text here for none ratings]"

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

        result["target"] = ratings_target(indicator) or evaluate_indicator(target, base_val, cur_val)
        if ratings_comments(indicator):
            commentary = ratings_comments(indicator)
        else:
            if indicator in gov_commentary_text:
                if "all" in gov_commentary_text[indicator]:
                    commentary = gov_commentary_text[indicator]["all"]
                else:
                    target_value = result["target"]
                    if target_value == None:
                        commentary = "Missing Data"
                    elif target_value == "question":
                        commentary = rating_question_text
                    elif target_value == "none":
                        commentary = rating_none_text
                    else:
                        commentary = gov_commentary_text[indicator][target_value]
                
                #result["commentary"] = result["commentary"].encode("utf-8")
                try:
                    result["commentary"] = commentary % result
                except TypeError:
                    result["commentary"] = None

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
        result = "cross"
        if indicator in ["1DP", "6DP", "7DP"]:
            if cur_val > 0: result = "tick" 
        elif indicator == "8DP":
            try:
                fix = Country8DPFix.objects.get(agency=agency, country=country)
                if fix.latest_progress:
                    result = "tick"
            except Country8DPFix.DoesNotExist:
                result = "cross"
        else:
            target = targets[indicator]
            result = evaluate_indicator(target, base_val, cur_val)
        indicators[indicator] = result
    return indicators

def country_agency_progress(country, agency):
    """
    Returns True is an agency is making progress in a particular country
    Progress is defined as # ticks / # ratings
    """
    ratings = country_agency_indicator_ratings(country, agency)
    ticks = filter(lambda x : x == "tick", ratings.values())
    return len(ticks) / float(len(ratings)) > 0.5

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
