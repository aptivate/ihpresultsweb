from collections import defaultdict
from math import fabs

from django.http import HttpResponse
from django.views.generic.simple import direct_to_template

from models import Submission, AgencyCountries, Agency, DPQuestion, GovQuestion, Country
from target import calc_agency_targets, get_country_progress, calc_country_targets, get_agency_progress
from indicators import calc_country_indicators, calc_agency_country_indicators

def agency_scorecard(request, template_name="submissions/agency_scorecard.html", extra_context=None):
    extra_context = extra_context or {}

    targets = {} 
    for agency in Agency.objects.filter(type="Agency").filter(updateagency__update=True):
        submissions = agency.submission_set.filter(type="DP")
        if submissions.count() == 0: continue
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
    extra_context["questions"] = DPQuestion.objects.filter(
        submission__agency__updateagency__update=True
    ).order_by("submission__agency", "submission__country", "question_number")
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def country_scorecard(request, template_name="submissions/country_scorecard.html", extra_context=None):
    def safe_div(val1, val2):
        try:
            if val1 == None or val2 == None:
                return None
            if val2 == 0:
                return 0
            return float(val1) / float(val2)
        except ValueError:
            return None

    def safe_diff(val1, val2):
        try:
            if val1 == None or val2 == None:
                return None
            if val2 == 0:
                return 0
            return float(val1) - float(val2)
        except ValueError:
            return None

    extra_context = extra_context or {}

    targets = {} 
    for country in Country.objects.all():
        submissions = country.submission_set.filter(type="Gov")
        if submissions.count() == 0: continue
        assert submissions.count() == 1

        submission = submissions.all()[0] 

        # don't process if the update flag is set to false
        if not submission.agency.updateagency.update:
            continue

        # Do not process if there are no questions
        if submission.govquestion_set.all().count() == 0: continue
        
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
        targets[country]["indicators"]["3G"]["hs_budget_gap"] = safe_diff(15, targets[country]["indicators"]["3G"]["latest_value"])
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

        def calc_change(val1, val2):
            try:
                if val1 == None or val2 == None:
                    return None, None
                val1 = float(val1)
                val2 = float(val2)
                val = val1 / val2 - 1
                if val < 0:
                    dir = "down"
                elif val > 0:
                    dir = "up"
                else:
                    dir = "no change"
                return fabs(val) * 100, dir
            except ValueError:
                return None, None

        other_indicators = targets[country]["indicators"]["other"]
        baseline_denom = safe_div(questions["18"]["baseline_value"], 10000.0)
        latest_denom = safe_div(questions["18"]["latest_value"], 10000.0)
        other_indicators["outpatient_visits_baseline"] = safe_div(questions["19"]["baseline_value"], baseline_denom)
        other_indicators["outpatient_visits_latest"] = safe_div(questions["19"]["latest_value"], latest_denom)
        other_indicators["outpatient_visits_change"], other_indicators["outpatient_visits_change_dir"] = calc_change(other_indicators["outpatient_visits_latest"], other_indicators["outpatient_visits_baseline"])
        other_indicators["skilled_personnel_baseline"] = safe_div(questions["17"]["baseline_value"], baseline_denom)
        other_indicators["skilled_personnel_latest"] = safe_div(questions["17"]["latest_value"], latest_denom)
        other_indicators["skilled_personnel_change"], other_indicators["skilled_personnel_change_dir"] = calc_change(other_indicators["skilled_personnel_latest"], other_indicators["skilled_personnel_baseline"])
        other_indicators["health_workforce_spent_change"], other_indicators["health_workforce_spent_change_dir"] = calc_change(questions["20"]["latest_value"], questions["20"]["baseline_value"])
        other_indicators["pfm_diff"] = safe_diff(questions["9"]["latest_value"], questions["9"]["baseline_value"])
        
        def sum_agency_values(question_number, field):
            sum = 0
            for agency in aval:
                if question_number in aval[agency]:
                    try:
                        sum += float(aval[agency][question_number][field])
                    except ValueError:
                        pass
            return sum

        coordinated_programmes = safe_diff(sum_agency_values("5", "latest_value"), sum_agency_values("4", "latest_value"))
        if coordinated_programmes > 0.51:
            other_indicators["coordinated_programmes"] = "tick"
        elif coordinated_programmes >= 0.11:
            other_indicators["coordinated_programmes"] = "arrow"
        else:
            other_indicators["coordinated_programmes"] = "cross"

    extra_context["targets"] = targets

    return direct_to_template(request, template=template_name, extra_context=extra_context)

def gov_questionnaire(request, template_name="submissions/gov_questionnaire.html", extra_context=None):

    extra_context = extra_context or {}
    extra_context["questions"] = GovQuestion.objects.filter(
        submission__agency__updateagency__update=True
    )
    return direct_to_template(request, template=template_name, extra_context=extra_context)
