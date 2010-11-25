from collections import defaultdict
import traceback
from math import fabs

from django.http import HttpResponse
from django.views.generic.simple import direct_to_template

from models import Submission, AgencyCountries, Agency, DPQuestion, GovQuestion, Country
from target import calc_agency_targets, get_country_progress, calc_country_targets, get_agency_progress
from indicators import calc_country_indicators, calc_agency_country_indicators

def get_agency_scorecard_data(agency):
    """
    Return data relevant to this agency's submissions
    Returns None if no submission has yet been submitted
    """

    submissions = agency.submission_set.filter(type="DP")
    if submissions.count() == 0: return None

    agency_data = calc_agency_targets(agency)

    # Include aggegated comments
    for indicator, d in agency_data.items():
        old_comments = d["comments"]
        comments = []
        for question_number, country, comment in old_comments:
            comments.append("%s %s] %s" % (question_number, country, comment))
        d["comments"] = "\n".join([comment for comment in comments if comment])
        d["key"] = "%s_%s" % (agency, indicator)
    # TODO Still need to add the erb data - i.e. consolidated comments 

    # Include a list of countries in which progress isn't/is being made
    agency_data["np"], agency_data["p"] = get_country_progress(agency)

    return agency_data

def get_agencies_scorecard_data():
    return dict([(agency, get_agency_scorecard_data(agency))
        for agency in Agency.objects.filter(type="Agency")
        if agency.submission_set.filter(type="DP").count() > 0
    ])

def agency_scorecard(request, template_name="submissions/agency_scorecard.html", extra_context=None):
    extra_context = extra_context or {}
    extra_context["targets"] = get_agencies_scorecard_data()

    return direct_to_template(request, template=template_name, extra_context=extra_context)

def agency_export(request):
    import csv

    headers = [
        "file", "agency", "profile", 
        "er1", "r1", "er2a", "r2a", "er2b", "r2b", "er2c", "r2c",
        "er3", "r3", "er4", "r4", "er5a", "r5a", "er5b", "r5b", "er5c", "r5c",
        "er6", "r6", "er7", "r7", "er8", "r8",
        "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10",
        "np1", "np2", "np3", "np4", "np5", "np6", "np7", "np8", "np9", "np10",
        "erb1", "erb2", "erb3", "erb4", "erb5", "erb6", "erb7", "erb8"
    ]

    default_text = "Insufficient data has been provided to enable a rating for this Standard Performance Measure."
    commentary_none = lambda commentary : commentary if commentary else default_text
    target_none = lambda target : target if target else "question"

    data = get_agencies_scorecard_data()
    for agency, datum in data.items():
        try:
            datum["file"] = agency.agency
            datum["agency"] = agency.agency 
            datum["profile"] = agency.description
            for indicator in ["1DP", "2DPa", "2DPb", "2DPc", 
                "3DP", "4DP", "5DPa", "5DPb", "5DPc", "6DP", "7DP", "8DP"]:

                h = indicator.replace("DP", "")
                datum["er%s" % h] = commentary_none(datum[indicator]["commentary"])
                datum["r%s" % h] = target_none(datum[indicator]["target"])

            for i in range(1, 9):
                # TODO - still need to add this stuff
                datum["erb%d" % i] = "Nothing yet"
            for i, val in datum["p"].items():
                datum["p%d" % (i + 1)] = val
            for i, val in datum["np"].items():
                datum["np%d" % (i + 1)] = val

        except Exception, e:
            traceback.print_exc()

    response = HttpResponse(mimetype="text/csv")
    response["Content-Disposition"] = "attachment; filename=agency_export.csv"
    writer = csv.writer(response)
    writer.writerow(headers)
    for agency in data:
        writer.writerow([data[agency].get(header, "") for header in headers])
    return response

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
