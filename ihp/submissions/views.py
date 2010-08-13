from collections import defaultdict

from django.http import HttpResponse
from django.views.generic.simple import direct_to_template

from models import Submission, AgencyCountries, Agency, DPQuestion, GovQuestion, Country
from target import calc_agency_targets, get_country_progress, calc_country_targets, get_agency_progress

def agency_scorecard(request, template_name="submissions/agency_scorecard.html", extra_context=None):
    extra_context = extra_context or {}

    targets = {} 
    for agency in Agency.objects.all():
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
        for question in GovQuestion.objects.filter(submission__country=country):
            qvals = targets[country]["questions"][question.question_number] = {}
            qvals["baseline_year"] = question.baseline_year
            qvals["baseline_value"] = question.baseline_value
            qvals["latest_year"] = question.latest_year
            qvals["latest_value"] = question.latest_value
            qvals["comments"] = question.comments
    #print targets
    extra_context["targets"] = targets

    return direct_to_template(request, template=template_name, extra_context=extra_context)

def gov_questionnaire(request, template_name="submissions/gov_questionnaire.html", extra_context=None):

    extra_context = extra_context or {}
    extra_context["questions"] = GovQuestion.objects.all()
    return direct_to_template(request, template=template_name, extra_context=extra_context)
