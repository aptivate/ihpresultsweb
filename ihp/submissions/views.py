from collections import defaultdict
import traceback
from math import fabs
import unicodecsv as csv

from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404
from django.utils.translation import check_for_language

from models import Submission, AgencyCountries, Agency, DPQuestion, GovQuestion, Country, MDGData, DPScorecardSummary, AgencyWorkingDraft, CountryWorkingDraft, Rating, Language
from target import calc_agency_ratings, get_country_progress, calc_country_ratings, get_agency_progress, country_agency_indicator_ratings, country_agency_progress, agency_country_indicator_ratings
from indicators import calc_country_indicators, calc_agency_country_indicators, NA_STR, calc_country_indicators, positive_funcs, dp_indicators, g_indicators, indicator_questions
from forms import DPSummaryForm, DPRatingsForm, GovRatingsForm, CountryScorecardForm
from utils import none_num, fformat_none, fformat_front, fformat_two
import translations
import country_scorecard
import agency_scorecard
from table_views import *

def agency_export(request, language):
    language = get_object_or_404(Language, language=language)

    headers = [
        "file", "agency", "agencytitle", "profile", 
        "er1", "r1", "er2a", "r2a", "er2b", "r2b", "er2c", "r2c",
        "er3", "r3", "er4", "r4", "er5a", "r5a", "er5b", "r5b", "er5c", "r5c",
        "er6", "r6", "er7", "r7", "er8", "r8",
        "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10",
        "np1", "np2", "np3", "np4", "np5", "np6", "np7", "np8", "np9", "np10",
        "erb1", "erb2", "erb3", "erb4", "erb5", "erb6", "erb7", "erb8",
        "workingdraft",
    ]

    response = HttpResponse(mimetype="text/csv")
    response["Content-Disposition"] = "attachment; filename=agency_export.csv"
    writer = csv.writer(response)
    writer.writerow(headers)

    for agency in Agency.objects.all():
        data = agency_scorecard.get_agency_scorecard_data(agency, language)
        writer.writerow([
            unicode(data.get(header, "")) for header in headers
        ])
    return response

def agency_alternative_baselines(request, template_name="submissions/agency_alternative_baselines.html", extra_context=None):
    """
    View that shows a histogram of the baseline years for a number of indicators
    """
    extra_context = extra_context or {}

    agencies = Agency.objects.all()
    questions = DPQuestion.objects.filter(submission__agency__in=agencies)
    is_2005 = lambda q: q.baseline_year == "2005"
    is_2007 = lambda q: q.baseline_year == "2007"
    is_other = lambda q: not (is_2005(q) or is_2007(q))

    counts = {}
    for indicator in ["2DPa", "2DPb", "2DPc", "5DPa", "5DPb"]:
        question_numbers = indicator_questions[indicator]
        questions_subset = questions.filter(question_number__in=question_numbers)
        counts["%s_2005" % indicator] = len(filter(is_2005, questions_subset))
        counts["%s_2007" % indicator] = len(filter(is_2007, questions_subset))
        counts["%s_other" % indicator] = len(filter(is_other, questions_subset))
        
    extra_context["counts"] = counts
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def agency_response_breakdown(request, template_name="submissions/agency_response_breakdown.html", extra_context=None):
    """
    Return a histogram of responses for each agency indicator 
    """

    extra_context = extra_context or {}
    is_na = lambda r : r == Rating.NONE
    is_question = lambda r : r == Rating.QUESTION
    is_response = lambda r : not (is_na(r) or is_question(r))

    agencies = Agency.objects.all()
    counts = defaultdict(int, {})
    for agency in agencies:
        for country in agency.countries:
            results = country_agency_indicator_ratings(country, agency)
            for indicator in dp_indicators:
                counts["%s_na" % indicator] += 1 if is_na(results[indicator]) else 0 
                counts["%s_question" % indicator] += 1 if is_question(results[indicator]) else 0 
                counts["%s_response" % indicator] += 1 if is_response(results[indicator]) else 0 
                counts["%s_total" % indicator] += 1 
    extra_context["counts"] = counts    
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def country_response_breakdown(request, template_name="submissions/country_response_breakdown.html", extra_context=None):
    """
    Return a histogram of responses for each country indicator 
    """

    extra_context = extra_context or {}
    is_na = lambda r : r["target"] == Rating.NONE
    is_question = lambda r : r["target"] == Rating.QUESTION
    is_response = lambda r : not (is_na(r) or is_question(r))

    countries = Country.objects.all()
    counts = defaultdict(int, {})
    for country in countries:
        results = calc_country_ratings(country)
        for indicator in g_indicators:
            counts["%s_na" % indicator] += 1 if is_na(results[indicator]) else 0 
            counts["%s_question" % indicator] += 1 if is_question(results[indicator]) else 0 
            counts["%s_response" % indicator] += 1 if is_response(results[indicator]) else 0 
            counts["%s_total" % indicator] += 1 
    extra_context["counts"] = counts    
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def dp_questionnaire(request, template_name="submissions/dp_questionnaire.html", extra_context=None):

    extra_context = extra_context or {}
    extra_context["questions"] = DPQuestion.objects.all().order_by(
        "submission__agency", 
        "submission__country", 
        "question_number"
    )
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def country_export(request, language):
    language = get_object_or_404(Language, language=language)
    headers = [
        # Front of scorecard
        "file", "TB2", "CD1", "CD2", "HSP1", "HSP2",
        "HSM1", "HSM2", "HSM3", "HSM4",
        "BC1", "BC2", "BC3", "BC4", "BC5", "BC6", "BC7", "BC8", "BC9", "BC10",
        "PC1", "PC2", "PC3", "PC4",
        "PF1", "PF2", "PFM1", "PFM2", "PR1", "PR2",
        "TA1", "TA2", "PHC1", "PHC2", "PHC3", "PHC4", "PHC5", "PHC6", "PHC7",
        "HRH1", "HRH2", "HRH3", "HRH4", "HRH5", "HRH6", "HRH7",
        "HS1", "HS2", "HS3", "HS4", "HS5", "HS6", "HS7",
        "RF1", "RF2", "RF3",
        "HMIS1", "HMIS2",
        "JAR1", "JAR2", "JAR3", "JAR4", "JAR5",
        "DBR1", "DBR2",
        "MDG1a", "MDG1b", "MDG1c", "MDG1d", "MDG1e",
        "MDG2a", "MDG2b", "MDG2c", "MDG2d", "MDG2e",
        "MDG3a", "MDG3b", "MDG3c", "MDG3d", "MDG3e",
        "MDG4a", "MDG4b", "MDG4c", "MDG4d", "MDG4e",
        "MDG5a1", "MDG5a2", "MDG5a3", "MDG5a4", "MDG5a5",
        "MDG5b1", "MDG5b2", "MDG5b3", "MDG5b4", "MDG5b5",
        "MDG6a1", "MDG6a2", "MDG6a3", "MDG6a4", "MDG6a5",
        "MDG6b1", "MDG6b2", "MDG6b3", "MDG6b4", "MDG6b5",
        "MDG6c1", "MDG6c2", "MDG6c3", "MDG6c4", "MDG6c5",
        "MDG7a1", "MDG7a2", "MDG7a3", "MDG7a4", "MDG7a5",
        "MDG7b1", "MDG7b2", "MDG7b3", "MDG7b4", "MDG7b5",
        
        # Back of scorecard
        "F1", "CN1", "GN1",
        "ER1a", "ER1b", "ER2a", "ER2b", "ER3a", "ER3b", "ER4a", "ER4b", "ER4c", "ER5a", "ER5b",
        "ER6a", "ER6b", "ER7a", "ER7b", "ER8a", "ER8b", "ER9a", "ER9b", "ER10a", "ER10b",
        "Header",
        "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11", "P12", "P13",
        "Header",
        "NP1", "NP2", "NP3", "NP4", "NP5", "NP6", "NP7", "NP8", "NP9", "NP10", "NP11", "NP12", "NP13",

        "workingdraft",
    ]

    special_formatting = {
       "HSM2" : fformat_none, 
       "BC2" : fformat_front, 
       "BC4" : fformat_front, 
       "PC1" : fformat_front, 
       "PC2" : fformat_front, 
       "PF1" : fformat_none, 
       "PHC1" : fformat_front, 
       "PHC3" : fformat_front, 
       "PHC5" : fformat_front, 
       "HRH1" : fformat_front, 
       "HRH3" : fformat_front, 
       "HRH5" : fformat_front, 
       "HS1" : fformat_front, 
       "HS3" : fformat_front, 
       "HS5" : fformat_front, 
       "RF2" : fformat_front, 
       "RF3" : fformat_front, 
    }
    def special_format(header, val):
        if header in special_formatting:
            return special_formatting[header](val)
        else:
            return val

    response = HttpResponse(mimetype="text/csv")
    response["Content-Disposition"] = "attachment; filename=country_export.csv"
    writer = csv.writer(response)
    writer.writerow(headers)

    for country in Country.objects.all():
        data = country_scorecard.get_country_export_data(country, language)
        writer.writerow([
            special_format(header, data.get(header, "")) for header in headers
        ])
    return response

def gov_questionnaire(request, template_name="submissions/gov_questionnaire.html", extra_context=None):

    extra_context = extra_context or {}
    extra_context["questions"] = GovQuestion.objects.all()
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def dp_summary_edit(request, template_name="submissions/dp_summary_edit.html", extra_context=None):
    extra_context = extra_context or {}

    if request.method == "POST":
        form = DPSummaryForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = DPSummaryForm()

    extra_context["form"] = form
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def dp_ratings_edit(request, template_name="submissions/dp_ratings_edit.html", extra_context=None):
    extra_context = extra_context or {}

    if request.method == "POST":
        form = DPRatingsForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = DPRatingsForm()

    extra_context["form"] = form
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def gov_ratings_edit(request, template_name="submissions/gov_ratings_edit.html", extra_context=None):
    extra_context = extra_context or {}

    if request.method == "POST":
        form = GovRatingsForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = GovRatingsForm()

    extra_context["form"] = form
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def agency_country_ratings(request, template_name="submissions/agency_country_ratings.html", extra_context=None):
    extra_context = extra_context or {}
    data = []
    for agency in Agency.objects.all().order_by("agency"):
        for country in agency.countries:
            ratings = country_agency_indicator_ratings(country, agency)
            making_progress = country_agency_progress(country, agency)

            data.append({
                "agency" : agency,
                "country" : country,
                "indicators" : ratings,
                "making_progress" : making_progress,
            })
    
    extra_context["data"] = data
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def country_scorecard_ratings_edit(request, template_name="submissions/country_scorecard_ratings_edit.html", extra_context=None):
    extra_context = extra_context or {}

    if request.method == "POST":
        form = CountryScorecardForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = CountryScorecardForm()

    extra_context["form"] = form
    return direct_to_template(request, template=template_name, extra_context=extra_context)
