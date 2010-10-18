from collections import defaultdict
from math import fabs

from django.http import HttpResponse
from django.views.generic.simple import direct_to_template

from models import Submission, AgencyCountries, Agency, DPQuestion, GovQuestion, Country
from target import calc_agency_targets, get_country_progress, calc_country_targets, get_agency_progress
from indicators import calc_country_indicators

def agency_scorecard(request, template_name="submissions/agency_scorecard.html", extra_context=None):
    extra_context = extra_context or {}

    targets = {} 
    for agency in Agency.objects.filter(type="Agency"):
        if agency.submission_set.count() == 0: continue
        targets[agency] = calc_agency_targets(agency)
        for indicator, d in targets[agency].items():
            old_comments = d["comments"]
            comments = []
            for question_number, country, comment in old_comments:
                comments.append("%s %s] %s" % (question_number, country, comment))
            d["comments"] = "\n".join([comment for comment in comments if comment])
            d["key"] = "%s_%s" % (agency, indicator)
        targets[agency]["np"], targets[agency]["p"] = get_country_progress(agency)
        
        extra_context["targets"] = targets

    return direct_to_template(request, template=template_name, extra_context=extra_context)

def dp_questionnaire(request, template_name="submissions/dp_questionnaire.html", extra_context=None):

    extra_context = extra_context or {}
    extra_context["questions"] = DPQuestion.objects.all()
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def country_scorecard(request, template_name="submissions/country_scorecard.html", extra_context=None):
    extra_context = extra_context or {}

    targets = {} 
    for country in Country.objects.all():
        if country.submission_set.count() == 0: continue
        country_target = calc_country_targets(country)
        if country_target == None: continue
        targets[country] = country_target
        
        for indicator, d in targets[country].items():
            old_comments = d["comments"]
            comments = []
            for question_number, country, comment in old_comments:
                comments.append("%s ] %s" % (question_number, comment))
            d["comments"] = "\n".join([comment for comment in comments if comment])
            d["key"] = "%s_%s" % (country, indicator)
        targets[country]["np"], targets[country]["p"] = get_agency_progress(country)
        targets[country]["questions"] = {}

        # Add indicators
        indicators = calc_country_indicators(country)
        headings = ["baseline_value", "baseline_year", "latest_value", "latest_year"]
        targets[country]["indicators"] = {}
        for indicator in indicators:
            targets[country]["indicators"][indicator] = dict(zip(headings, indicators[indicator][0]))
        targets[country]["indicators"]["3G"]["hs_budget_gap"] = 15 - targets[country]["indicators"]["3G"]["latest_value"]
        targets[country]["indicators"]["other"] = {}
        

        # Add agency submissions
        agencies = AgencyCountries.objects.get_country_agencies(country)
        aval = targets[country]["agencies"] = {}
        for agency in agencies:
            aval[agency.agency] = {}
            for question in DPQuestion.objects.filter(submission__agency=agency, submission__country=country):
                qvals = aval[agency.agency][question.question_number] = {}
                qvals["baseline_year"] = question.baseline_year
                qvals["baseline_value"] = question.baseline_value
                qvals["latest_year"] = question.latest_year
                qvals["latest_value"] = question.latest_value
                qvals["comments"] = question.comments

        for question in GovQuestion.objects.filter(submission__country=country):
            qvals = targets[country]["questions"][question.question_number] = {}
            qvals["baseline_year"] = question.baseline_year
            qvals["baseline_value"] = question.baseline_value
            qvals["latest_year"] = question.latest_year
            qvals["latest_value"] = question.latest_value
            qvals["comments"] = question.comments

        questions = targets[country]["questions"]
        def safe_div(val1, val2):
            if val1 == None or val2 == None:
                return None
            if val2 == 0:
                return 0
            return float(val1) / float(val2)

        def safe_diff(val1, val2):
            if val1 == None or val2 == None:
                return None
            if val2 == 0:
                return 0
            return float(val1) - float(val2)

        def calc_change(val1, val2):
            val1 = float(val1)
            val2 = float(val2)
            val = val1 / val2 - 1
            if val < 0:
                dir = "decrease"
            elif val > 0:
                dir = "increase"
            else:
                dir = "no change"
            return fabs(val) * 100, dir

        other_indicators = targets[country]["indicators"]["other"]
        baseline_denom = safe_div(questions["18"]["baseline_value"], 10000.0)
        latest_denom = safe_div(questions["18"]["latest_value"], 10000.0)
        other_indicators["outpatient_visits_baseline"] = safe_div(questions["19"]["baseline_value"], baseline_denom)
        other_indicators["outpatient_visits_latest"] = safe_div(questions["19"]["latest_value"], latest_denom)
        other_indicators["outpatient_visits_change"], _ = calc_change(other_indicators["outpatient_visits_latest"], other_indicators["outpatient_visits_baseline"])
        other_indicators["skilled_personnel_baseline"] = safe_div(questions["17"]["baseline_value"], baseline_denom)
        other_indicators["skilled_personnel_latest"] = safe_div(questions["17"]["latest_value"], latest_denom)
        other_indicators["skilled_personnel_change"], _ = calc_change(other_indicators["skilled_personnel_latest"], other_indicators["skilled_personnel_baseline"])
        other_indicators["health_workforce_spent_change"], _ = calc_change(questions["20"]["latest_value"], questions["20"]["baseline_value"])
        other_indicators["pfm_diff"] = safe_diff(questions["9"]["latest_value"], questions["9"]["baseline_value"])
    extra_context["targets"] = targets

    return direct_to_template(request, template=template_name, extra_context=extra_context)

def gov_questionnaire(request, template_name="submissions/gov_questionnaire.html", extra_context=None):

    extra_context = extra_context or {}
    extra_context["questions"] = GovQuestion.objects.all()
    return direct_to_template(request, template=template_name, extra_context=extra_context)
