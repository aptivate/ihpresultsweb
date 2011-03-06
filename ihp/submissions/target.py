#-*- coding: utf-8 -*-
import numbers
from django.template import Context, Template
from django.utils.functional import memoize
from indicators import NA_STR
<<<<<<< HEAD
from indicators import calc_agency_indicators, calc_country_indicators, dp_indicators, g_indicators, calc_agency_country_indicators
from models import AgencyTargets, AgencyCountries, Submission, CountryTargets, Country8DPFix, GovScorecardRatings, GovScorecardComments, DPScorecardRatings, Rating, Language
import models
=======
from indicators import (calc_agency_indicators, calc_country_indicators,
    dp_indicators, g_indicators, calc_agency_country_indicators,
    calc_country_agency_indicators)
from models import AgencyTargets, AgencyCountries, Submission, CountryTargets, Country8DPFix, GovScorecardRatings, CountryLanguage, DPScorecardRatings, Rating
>>>>>>> 5f1ff12ad8406b128e8985ffc7b8a607f65fb201
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

def calc_agency_ratings(agency, language=None):
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

    language = language or models.Language.objects.get(language="English")
    translation = translations.get_translation(language)

    def ratings_val(obj, tmpl):
        def _func(indicator):
            h = indicator.replace("DP", "")
            d = obj.__dict__
            return d.get(tmpl % h, None)
        return _func

    def round_to_zero(x):
        if type(x) == float and round(x, 0) == 0:
            return 0.0
        else:
            return x


    targets = get_agency_targets(agency, dp_indicators)
    indicators = calc_agency_indicators(agency)
    ratings, _ = models.DPScorecardRatings.objects.get_or_create(agency=agency)
    comments_override, _ = models.DPScorecardComments.objects.get_or_create(agency=agency, language=language)
    results = {}
    ratings_comments = ratings_val(comments_override, "er%s")
    ratings_target = ratings_val(ratings, "r%s")

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
                template = translation.agency_commentary_text[indicator]
                if type(template) == Template:
                    result["commentary"] = template.render(Context(result))
                else:
                    result["commentary"] = template % result
            except:
                pass

            if result["target"] == Rating.NONE:
            #if NA_STR in [base_val, cur_val]:
                result["commentary"] = translation.rating_none_text % agency.agency
            elif result["commentary"] == "":
                result["commentary"] = translation.rating_question_text

        results[indicator] = result

    return results

def calc_country_ratings(country, language=None):
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
    language = language or models.Language.objects.get(language="English")

    translation = translations.get_translation(language)
    gov_commentary_text = translation.gov_commentary_text

    rating_question_text = translation.rating_question_text
    rating_none_text = translation.rating_none_text % country.country

    targets = get_country_targets(country, g_indicators)
    indicators = calc_country_indicators(country)
    results = {}
    ratings, _ = models.GovScorecardRatings.objects.get_or_create(country=country)
    comment_override, _ = models.GovScorecardComments.objects.get_or_create(country=country, language=language)

    def ratings_val(obj, tmpl):
        def _func(indicator):
            h = indicator.replace("G", "").replace("Q", "")
            d = obj.__dict__
            return d.get(tmpl % h, None)
        return _func

    ratings_comments = ratings_val(comment_override, "er%s")
    ratings_target = ratings_val(ratings, "r%s")

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
                
                try:
                    result["commentary"] = commentary % result
                except TypeError, e:
                    result["commentary"] = ["This text couldn't be generated, possibly because the rating was overriden. Please override the text appropriately as well"]

        results[indicator] = result
    return results

def calc_country_scorecard_values(country, language):
    """
    Calculate values needed by country scorecard
    """
    data = calc_country_ratings(country, language)
    country_questions = models.GovQuestion.objects.filter(submission__country=country)

    lang = language.language
    comments, _ = models.CountryScorecardOverrideComments.objects.get_or_create(
        country=country, language=language
    )

    data["rf2_%s" % lang] = comments.rf2 or country_questions.filter(question_number="22")[0].latest_value
    data["rf3_%s" % lang] = comments.rf3 or country_questions.filter(question_number="23")[0].latest_value
    data["dbr2_%s" % lang] = comments.dbr2 or country_questions.filter(question_number="11")[0].comments
    data["hmis2_%s" % lang] = comments.hmis2 or country_questions.filter(question_number="21")[0].comments
    jar4_question = country_questions.filter(question_number="24")[0]
    data["jar4_%s" % lang] = comments.jar4 or "Latest Value: %s\nComment: %s" % (jar4_question.latest_value, jar4_question.comments)
    data["pfm2_%s" % lang] = comments.pfm2 or country_questions.filter(question_number="9")[0].comments
    data["pr2_%s" % lang] = comments.pr2 or country_questions.filter(question_number="10")[0].comments
    data["pf2_%s" % lang] = comments.pf2 or country_questions.filter(question_number="16")[0].comments
    data["cd2_%s" % lang] = comments.cd2 or country_questions.filter(question_number="1")[0].comments

    tmp_ta2 = ""
    for q in models.DPQuestion.objects.filter(submission__country=country, question_number="4"):
        tmp_ta2 += q.submission.agency.agency + ": " + q.comments + "\n\n"
    data["ta2_%s" % lang] = comments.ta2 or tmp_ta2
    return data

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

def agency_country_indicator_ratings(agency, country):
    """
    Evaluate ratings for an agency-country per indicator
    TODO this was copied and pasted from country_agency_indicator_ratings,
    check that it actually makes sense! 
    """
    indicators = {}
    targets = get_country_targets(country, g_indicators)
    agency_indicators = calc_country_agency_indicators(country, agency)

    for indicator in agency_indicators:
        v = agency_indicators[indicator]
        debug("extracting %s from %s" % (indicator, str(agency_indicators)))
        values, comments = v
        (base_val, base_year, cur_val, cur_year) = values
        # TODO this is a hack - it might be better to extract this
        # logic out of here
        result = None
        if indicator in ["1G", "6G", "7G"] and cur_val != NA_STR:
            if cur_val > 0: 
                result = Rating.TICK
            elif base_val == None and cur_val == None:
                result = Rating.QUESTION
            elif base_val in [None, NA_STR]:
                result = Rating.CROSS
        elif indicator == "8G":
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
