from collections import defaultdict
import traceback
from math import fabs
import unicodecsv as csv

from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404
from django.utils.translation import check_for_language

from models import Submission, AgencyCountries, Agency, DPQuestion, GovQuestion, Country, MDGData, DPScorecardSummary, AgencyWorkingDraft, CountryWorkingDraft, CountryScorecardOverride, Rating
from target import calc_agency_ratings, get_country_progress, calc_country_ratings, get_agency_progress, country_agency_indicator_ratings, country_agency_progress
from indicators import calc_country_indicators, calc_agency_country_indicators, NA_STR, calc_country_indicators, positive_funcs, dp_indicators, g_indicators, indicator_questions
from forms import DPSummaryForm, DPRatingsForm, GovRatingsForm, CountryScorecardForm
from utils import none_num

def get_agency_scorecard_data(agency):
    """
    Return data relevant to this agency's submissions
    Returns None if no submission has yet been submitted
    """

    submissions = agency.submission_set.filter(type="DP")
    if submissions.count() == 0: return None

    agency_data = calc_agency_ratings(agency)

    # Include aggegated comments
    for indicator, d in agency_data.items():
        old_comments = d["comments"]
        comments = []
        for question_number, country, comment in old_comments:
            comments.append("%s %s] %s" % (question_number, country, comment))
        d["comments"] = "\n".join([comment for comment in comments if comment])
        d["key"] = "%s_%s" % (agency, indicator)

    # Include a list of countries in which progress isn't/is being made
    agency_data["np"], agency_data["p"] = get_country_progress(agency)

    return agency_data

def get_agencies_scorecard_data(agencies=None):
    agencies = agencies or Agency.objects.all_types()
    return dict([(agency, get_agency_scorecard_data(agency))
        for agency in agencies
        if agency.submission_set.filter(type="DP").count() > 0
    ])

def get_country_scorecard_data(country):

    submissions = country.submission_set.filter(type="Gov")
    assert submissions.count() == 1

    submission = submissions.all()[0] 

    # Do not process if there are no questions
    if submission.govquestion_set.all().count() == 0: 
        raise Exception("Possible incomplete submission")
    
    country_data = calc_country_ratings(country)
    
    for indicator, d in country_data.items():
        old_comments = d["comments"]
        comments = []
        for question_number, country, comment in old_comments:
            comments.append("%s ] %s" % (question_number, comment))
        d["comments"] = "\n".join([comment for comment in comments if comment])
        d["key"] = "%s_%s" % (country, indicator)
    country_data["np"], country_data["p"] = get_agency_progress(country)
    country_data["questions"] = {}

    # Add indicators
    indicators = calc_country_indicators(country)
    country_data["indicators"] = {}
    for indicator in indicators:
        ind = country_data["indicators"][indicator] = {}
        data = indicators[indicator][0]
        ind["baseline_value"] = none_num(data[0])
        ind["baseline_year"] = data[1]
        ind["latest_value"] = none_num(data[2])
        ind["latest_year"] = data[3]

    #TODO hack
    if country_data["indicators"]["3G"]["latest_value"] != NA_STR:
        country_data["indicators"]["3G"]["hs_budget_gap"] = 15 - country_data["indicators"]["3G"]["latest_value"]
    else:
        country_data["indicators"]["3G"]["hs_budget_gap"] = None
    country_data["indicators"]["other"] = {}

    # Add agency submissions
    agencies = AgencyCountries.objects.get_country_agencies(country)
    aval = country_data["agencies"] = {}
    for agency in agencies:
        aval[agency.agency] = {}
        for question in DPQuestion.objects.filter(submission__agency=agency, submission__country=country):
            qvals = aval[agency.agency][question.question_number] = {}
            qvals["baseline_year"] = question.baseline_year
            qvals["baseline_value"] = question.base_val
            qvals["latest_year"] = question.latest_year
            qvals["latest_value"] = question.cur_val
            qvals["comments"] = question.comments

    for question in GovQuestion.objects.filter(submission__country=country):
        qvals = country_data["questions"][question.question_number] = {}
        qvals["baseline_year"] = question.baseline_year
        qvals["latest_year"] = question.latest_year
        qvals["comments"] = question.comments

        qvals["baseline_value"] = none_num(question.base_val)
        qvals["latest_value"] = none_num(question.cur_val)

    questions = country_data["questions"]

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

    other_indicators = country_data["indicators"]["other"]
    baseline_denom = questions["18"]["baseline_value"] / 10000.0
    latest_denom = questions["18"]["latest_value"] / 10000.0

    # Outpatient Visits
    other_indicators["outpatient_visits_baseline"] = questions["19"]["baseline_value"] / baseline_denom
    other_indicators["outpatient_visits_latest"] = questions["19"]["latest_value"] / latest_denom
    other_indicators["outpatient_visits_change"], other_indicators["outpatient_visits_change_dir"] = calc_change(other_indicators["outpatient_visits_latest"], other_indicators["outpatient_visits_baseline"])

    # Skilled Personnel
    other_indicators["skilled_personnel_baseline"] = questions["17"]["baseline_value"] / baseline_denom
    other_indicators["skilled_personnel_latest"] = questions["17"]["latest_value"] / latest_denom
    other_indicators["skilled_personnel_change"], other_indicators["skilled_personnel_change_dir"] = calc_change(other_indicators["skilled_personnel_latest"], other_indicators["skilled_personnel_baseline"])

    # Health Workforce
    other_indicators["health_workforce_perc_of_budget_baseline"] = questions["20"]["baseline_value"] / questions["7"]["baseline_value"]
    other_indicators["health_workforce_perc_of_budget_latest"] = questions["20"]["latest_value"] / questions["7"]["latest_value"]
    other_indicators["health_workforce_spent_change"], other_indicators["health_workforce_spent_change_dir"] = calc_change(questions["20"]["latest_value"], questions["20"]["baseline_value"])

    other_indicators["pfm_diff"] = questions["9"]["latest_value"] - questions["9"]["baseline_value"]
    
    def sum_agency_values(question_number, field):
        sum = 0
        for agency in aval:
            if question_number in aval[agency]:
                try:
                    sum += float(aval[agency][question_number][field])
                except ValueError:
                    pass
        return sum

    coordinated_programmes = sum_agency_values("5", "latest_value") - sum_agency_values("4", "latest_value")
    if coordinated_programmes > 0.51:
        other_indicators["coordinated_programmes"] = Rating.TICK
    elif coordinated_programmes >= 0.11:
        other_indicators["coordinated_programmes"] = Rating.ARROW
    else:
        other_indicators["coordinated_programmes"] = Rating.CROSS

    return country_data

def get_countries_scorecard_data():
    return dict([(country, get_country_scorecard_data(country))
        for country in Country.objects.all()
        if country.submission_set.filter(type="Gov").count() > 0
    ])

def agency_export_lang(request, language):
    if language and check_for_language(language):
        if hasattr(request, 'session'):
            request.session['django_language'] = language
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return agency_export(request)
    
def agency_export(request):

    headers = [
        "file", "agency", "profile", 
        "er1", "r1", "er2a", "r2a", "er2b", "r2b", "er2c", "r2c",
        "er3", "r3", "er4", "r4", "er5a", "r5a", "er5b", "r5b", "er5c", "r5c",
        "er6", "r6", "er7", "r7", "er8", "r8",
        "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10",
        "np1", "np2", "np3", "np4", "np5", "np6", "np7", "np8", "np9", "np10",
        "erb1", "erb2", "erb3", "erb4", "erb5", "erb6", "erb7", "erb8",
        "workingdraft",
    ]

    data = get_agencies_scorecard_data()
    for agency, datum in data.items():
        try:
            datum["file"] = agency.agency
            datum["agency"] = agency.agency 
            datum["profile"] = agency.description
            for indicator in dp_indicators:

                h = indicator.replace("DP", "")
                datum["er%s" % h] = datum[indicator]["commentary"]
                datum["r%s" % h] = datum[indicator]["target"]

            for i in range(1, 11):
                datum["p%d" % i] = datum["p"].get(i - 1, "pgreen")
                datum["np%d" % i] = datum["np"].get(i - 1, "npwhite")
            try:
                summary = DPScorecardSummary.objects.get(agency=agency)
                datum["erb1"] = summary.erb1
                datum["erb2"] = summary.erb2
                datum["erb3"] = summary.erb3
                datum["erb4"] = summary.erb4
                datum["erb5"] = summary.erb5
                datum["erb6"] = summary.erb6
                datum["erb7"] = summary.erb7
                datum["erb8"] = summary.erb8
            except DPScorecardSummary.DoesNotExist:
                pass

            working_draft, _ = AgencyWorkingDraft.objects.get_or_create(agency=agency)
            datum["workingdraft"] = "workingdraft" if working_draft.is_draft else ""

        except Exception, e:
            traceback.print_exc()

    response = HttpResponse(mimetype="text/csv")
    response["Content-Disposition"] = "attachment; filename=agency_export.csv"
    writer = csv.writer(response)
    writer.writerow(headers)
    for agency in data:
        writer.writerow([data[agency].get(header, "") for header in headers])
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

def formatter(decimals):
    def f(x):
        try:
            x = float(x)
            x = round(x, decimals)
            if decimals == 0: 
                return int(x)
            return x
        except ValueError, e:
            return x
        except TypeError, e:
            return x
    return f

fformat_front = formatter(1)
fformat_none = formatter(0)
fformat_two = formatter(2)

def get_countries_export_data():
    data = get_countries_scorecard_data()
    for country, datum in data.items():
        ratings, _ = CountryScorecardOverride.objects.get_or_create(country=country)
        try:
            datum["ER1a"] = datum["1G"]["target"]
            datum["ER1b"] = datum["1G"]["commentary"]
            datum["ER2a"] = datum["2Ga"]["target"]
            datum["ER2b"] = datum["2Ga"]["commentary"]
            datum["ER3a"] = datum["2Gb"]["target"]
            datum["ER3b"] = datum["2Gb"]["commentary"]
            datum["ER4a"] = datum["3G"]["target"]
            datum["ER4b"] = datum["3G"]["commentary"]
            datum["ER4c"] = country.country
            datum["ER5a"] = datum["4G"]["target"]
            datum["ER5b"] = datum["4G"]["commentary"]
            datum["ER6a"] = datum["5Ga"]["target"]
            datum["ER6b"] = datum["5Ga"]["commentary"]
            datum["ER7a"] = datum["5Gb"]["target"]
            datum["ER7b"] = datum["5Gb"]["commentary"]
            datum["ER8a"] = datum["6G"]["target"]
            datum["ER8b"] = datum["6G"]["commentary"]
            datum["ER9a"] = datum["7G"]["target"]
            datum["ER9b"] = datum["7G"]["commentary"]
            datum["ER10a"] = datum["8G"]["target"]
            datum["ER10b"] = datum["8G"]["commentary"]

            datum["file"] = country.country
            datum["TB2"] = "%s COUNTRY SCORECARD" % country.country.upper()

            datum["CD1"] = datum["ER1a"]
            datum["CD2"] = ratings.cd2 or datum["questions"]["1"]["comments"]
            datum["HSP1"] = ratings.hsp1 or datum["Q2G"]["target"]
            datum["HSP2"] = ratings.hsp2 or datum["Q3G"]["target"]
            datum["HSM1"] = ratings.hsm1 or datum["Q12G"]["target"]
            datum["HSM2"] = fformat_none(datum["questions"]["15"]["latest_value"])
            datum["HSM3"] = datum["ER10a"]
            datum["HSM4"] = ratings.hsm4

            datum["BC1"] = datum["questions"]["5"]["baseline_year"]
            datum["BC2"] = fformat_front(datum["questions"]["6"]["baseline_value"])
            datum["BC3"] = datum["questions"]["5"]["latest_year"]
            datum["BC4"] = fformat_front(datum["questions"]["6"]["latest_value"])
            datum["BC5"] = "?????"
            datum["BC6"] = "?????"
            datum["BC7"] = "?????"
            datum["BC8"] = "?????"
            datum["BC9"] = "?????"
            datum["BC10"] = "?????"

            datum["PC1"] = fformat_front(datum["indicators"]["3G"]["latest_value"])
            datum["PC2"] = fformat_front(datum["indicators"]["3G"]["hs_budget_gap"])
            datum["PC3"] = "%s %% allocated to health" % datum["PC1"]
            datum["PC4"] = "%s %% increase needed to meet the Abuja target (15%%)" % datum["PC2"]

            datum["PF1"] = fformat_none(datum["questions"]["16"]["latest_value"])
            datum["PF2"] = ratings.pf2 or datum["questions"]["16"]["comments"]

            datum["PFM1"] = datum["ER6a"]
            datum["PFM2"] = ratings.pfm2 or datum["questions"]["9"]["comments"]

            datum["PR1"] = datum["ER7a"]
            datum["PR2"] = ratings.pr2 or datum["questions"]["10"]["comments"]

            datum["TA1"] = datum["indicators"]["other"]["coordinated_programmes"]
            datum["TA2"] = ""
            for agency in datum["agencies"]:
                aqs = datum["agencies"][agency]
                if "4" in aqs:
                    datum["TA2"] += "%s %s" % (agency, aqs["4"]["comments"].replace("%", "%%"))
                    datum["TA2"] += "\n"
            datum["TA2"] = ratings.ta2 or datum["TA2"]

            datum["PHC1"] = fformat_front(datum["indicators"]["other"]["outpatient_visits_baseline"])
            datum["PHC2"] = datum["questions"]["19"]["baseline_year"]
            datum["PHC3"] = fformat_front(datum["indicators"]["other"]["outpatient_visits_latest"])
            datum["PHC4"] = datum["questions"]["19"]["latest_year"]
            datum["PHC5"] = fformat_front(datum["indicators"]["other"]["outpatient_visits_change"])
            datum["PHC6"] = datum["indicators"]["other"]["outpatient_visits_change_dir"]
            datum["PHC7"] = ""

            datum["HRH1"] = fformat_front(datum["indicators"]["other"]["skilled_personnel_baseline"])
            datum["HRH2"] = datum["questions"]["17"]["baseline_year"]
            datum["HRH3"] = fformat_front(datum["indicators"]["other"]["skilled_personnel_latest"])
            datum["HRH4"] = datum["questions"]["17"]["latest_year"]
            datum["HRH5"] = fformat_front(datum["indicators"]["other"]["skilled_personnel_change"])
            datum["HRH6"] = datum["indicators"]["other"]["skilled_personnel_change_dir"]
            datum["HRH7"] = ""

            datum["HS1"] = fformat_front(datum["questions"]["20"]["baseline_value"])
            datum["HS2"] = datum["questions"]["20"]["baseline_year"]
            datum["HS3"] = fformat_front(datum["questions"]["20"]["latest_value"])
            datum["HS4"] = datum["questions"]["20"]["latest_year"]
            datum["HS5"] = fformat_front(datum["indicators"]["other"]["health_workforce_spent_change"])
            datum["HS6"] = datum["indicators"]["other"]["health_workforce_spent_change_dir"]
            datum["HS7"] = ""

            datum["RF1"] = datum["ER8a"]
            datum["RF2"] = fformat_none(ratings.rf2 or datum["questions"]["22"]["latest_value"])
            datum["RF3"] = fformat_none(ratings.rf3 or datum["questions"]["23"]["latest_value"])

            datum["HMIS1"] = ratings.hmis1 or datum["Q21G"]["target"]
            datum["HMIS2"] = ratings.hmis2 or datum["questions"]["21"]["comments"]

            datum["JAR1"] = ratings.jar1 or datum["Q12G"]["target"]
            #datum["JAR2"] = ""
            #datum["JAR3"] = fformat_front(datum["questions"]["24"]["latest_value"])
            #datum["JAR4"] = datum["questions"]["24"]["comments"]
            #datum["JAR5"] = datum["questions"]["24"]["comments"]
            datum["JAR2"] = "Field no longer used"
            datum["JAR3"] = "Field no longer used"
            datum["JAR4"] = ratings.jar4 or datum["questions"]["24"]["comments"]
            datum["JAR5"] = "Field no longer used"

            datum["DBR1"] = datum["ER8a"]
            datum["DBR2"] = ratings.dbr2 or datum["questions"]["11"]["comments"]

            group1 = ["MDG1", "MDG2", "MDG3", "MDG4"]
            group2 = ["MDG5a", "MDG5b", "MDG6a", "MDG6b", "MDG6c", "MDG7a", "MDG7b"]
            group1_index = "abcde"
            group2_index = "12345"
            needs_percent = ["MDG1", "MDG2", "MDG6a", "MDG6b", "MDG7a", "MDG7b"]
            add_perc = lambda ind : "%" if ind in needs_percent else ""
            for mdg in group1 + group2:
                index = group1_index if mdg in group1 else group2_index

            
                mdgdata = MDGData.objects.get(mdg_target=mdg, country=country)
                if not mdgdata.latest_value:
                    datum[mdg + index[0]] = ""
                    datum[mdg + index[1]] = ""
                    datum[mdg + index[2]] = "questionmdg"
                    datum[mdg + index[3]] = ""
                    datum[mdg + index[4]] = ""
                elif not mdgdata.baseline_value:
                    datum[mdg + index[0]] = str(fformat_front(mdgdata.latest_value)) + add_perc(mdg)
                    datum[mdg + index[1]] = mdgdata.latest_year
                    datum[mdg + index[2]] = "questionmdg"
                    datum[mdg + index[3]] = ""
                    datum[mdg + index[4]] = ""
                else:
                    fmt = fformat_two if mdg == "MDG3" else fformat_front
            
                    datum[mdg + index[0]] = str(fmt(mdgdata.latest_value)) + add_perc(mdg)
                    datum[mdg + index[1]] = mdgdata.latest_year
                    datum[mdg + index[2]] = mdgdata.arrow
                    datum[mdg + index[3]] = str(fmt(mdgdata.change)) + add_perc(mdg)
                    datum[mdg + index[4]] = mdgdata.baseline_year

            datum["F1"] = country.country
            datum["CN1"] = datum["TB2"]
            datum["GN1"] = country.country

            datum["Header"] = country.country

            for i in range(1, 14):
                datum["P%d" % i] = datum["p"].get(i - 1, "pwhite")
                datum["NP%d" % i] = datum["np"].get(i - 1, "npwhite")

            working_draft, _ = CountryWorkingDraft.objects.get_or_create(country=country)
            datum["workingdraft"] = "workingdraft" if working_draft.is_draft else ""

        except Exception, e:
            traceback.print_exc()
    return data

def country_export(request, language):
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

    data = get_countries_export_data()

    response = HttpResponse(mimetype="text/csv")
    response["Content-Disposition"] = "attachment; filename=country_export.csv"
    writer = csv.writer(response)
    writer.writerow(headers)

    for country in data:
        writer.writerow([data[country].get(header, "") for header in headers])
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

def perc_change(base_val, latest_val):
    none_vals = [None, NA_STR]
    if type(base_val) == str or type(latest_val) == str:
        return None
    if base_val in none_vals or latest_val in none_vals:
        return None
    if base_val == 0:
        return None
    return (latest_val - base_val) / base_val * 100.0


spm_map = {
    #"1DP" : "Proportion of ihp+ countries in which the partner has signed commitment to (or documented support for) the ihp+ country compact, or equivalent agreement.",
    "1DP" : "Partner has signed commitment to (or documented support for) the IHP+ country compact, or equivalent agreement, where they exist.",
    "2DPa" : "Percent of aid flows to the health sector that is reported on national health sector budgets.",
    "2DPb" : "Percent of current capacity-development support provided through coordinated programmes consistent with national plans/strategies for the health sector.",
    "2DPc" : "Percent of health sector aid provided as programme based approaches.",
    "3DP" : "Percent of health sector aid provided through multi-year commitments.",
    "4DP" : "Percent of health sector aid disbursements released according to agreed schedules in annual or multi-year frameworks.",
    "5DPa" : "Percent of health sector aid that uses country procurement systems.",
    "5DPb" : "Percent of health sector aid that uses public financial management systems.",
    "5DPc" : "Number of parallel project implementation units (pius) per country.",
    #"6DP" : "Proportion of countries in which agreed, transparent and monitorable performance assessment frameworks are being used to assess progress in the health sector.",
    "6DP" : "Partner uses the single national performance assessment framework, where they exist, as the primary basis to assess progress (of support to health sector).",
    #"7DP" : "Proportion of countries where mutual assessments have been made of progress implementing commitments in the health sector, including on aid effectiveness.",
    "7DP" : "Partner has participated in mutual assessment of progress implementing commitments in the health sector, including on aid effectiveness, if a mutual assessment process exists.",
    "8DP" : "Evidence of support for civil society to be actively represented in health sector policy processes - including health sector planning, coordination & review mechanisms.",
}
        
gov_spm_map = {
    "1G" : "IHP+ Compact or equivalent mutual agreement in place.",
    "2Ga1" : "National Health Sector Plans/Strategy in place with current targets & budgets.",
    "2Ga2" : "National Health Sector Plans/Strategy in place with current targets & budgets that have been jointly assessed.",
    "2Gb" : "Costed and evidence-based HRH plan in place that is integrated with the national health plan.",
    "3G" : "Proportion of public funding allocated to health.",
    "4G" : "Proportion of health sector funding disbursed against the approved annual budget.",
    "5Ga" : "Public Financial Management systems for the health sector either (a) adhere to broadly accepted good practices or (b) have a reform programme in place to achieve these.",
    "5Gb" : "Country Procurement systems for the health sector either (a) adhere to broadly accepted good practices or (b) have a reform programme in place to achieve these.",
    "6G" : "An agreed transparent and monitorable performance assessment framework is being used to assess progress in the health sector.",
    "7G" : "Mutual Assessments, such as Joint Annual Health Sector Reviews, have been made of progress implementing commitments in the health sector, including on aid effectiveness.",
    "8G" : "Evidence that Civil Society is actively represented in health sector policy processes - including Health Sector planning, coordination & review mechanisms.",
}
        

def tbl_float_format(x, places=0):
    if type(x) == float:
        if places == 0:
            return int(round(x, places))
        else:
            return round(x, places) 
    elif x == NA_STR:
        return "N/A"
    elif x == None:
        return None
    return x

def agency_table_by_country(request, country_id, template_name="submissions/agency_table.html", extra_context=None):
    extra_context = extra_context or {} 
    country = get_object_or_404(Country, pk=country_id)

    abs_values = {}
    for agency in country.agencies:
        ratings = country_agency_indicator_ratings(country, agency)
        agency_abs_values = {}
        indicators = calc_agency_country_indicators(agency, country, positive_funcs)
        for indicator in indicators:
            base_val, base_year, latest_val, latest_year = indicators[indicator][0]
            agency_abs_values[indicator] = {
                "base_val" : tbl_float_format(base_val), 
                "latest_val" : tbl_float_format(latest_val), 
                "perc_change" : tbl_float_format(perc_change(base_val, latest_val)), 
                "base_year" : base_year,
                "latest_year" : latest_year,
                "rating" : ratings[indicator]
            } 
        abs_values[agency.agency] = agency_abs_values
    extra_context["abs_values"] = sorted(abs_values.items())
    extra_context["spm_map"] = spm_map
    extra_context["institution_name"] = "Development Partners in %s" % country.country
    
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def agency_table_by_agency(request, agency_id, template_name="submissions/agency_table.html", extra_context=None):
    extra_context = extra_context or {} 
    agency = get_object_or_404(Agency, pk=agency_id)

    abs_values = {}
    for country in agency.countries:
        country_abs_values = {}
        indicators = calc_agency_country_indicators(agency, country, positive_funcs)
        ratings = country_agency_indicator_ratings(country, agency)
        for indicator in indicators:
            base_val, base_year, latest_val, latest_year = indicators[indicator][0]
            country_abs_values[indicator] = {
                "base_val" : tbl_float_format(base_val), 
                "latest_val" : tbl_float_format(latest_val), 
                "perc_change" : tbl_float_format(perc_change(base_val, latest_val)),
                "base_year" : base_year,
                "latest_year" : latest_year,
                "rating" : ratings[indicator]
            } 
        abs_values[country.country] = country_abs_values
    extra_context["abs_values"] = sorted(abs_values.items())
    extra_context["spm_map"] = spm_map
    extra_context["institution_name"] = "%s Data across IHP+ Countries" % agency.agency
    
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def agency_table_by_indicator(request, indicator, template_name="submissions/agency_table_by_indicator.html", extra_context=None):
    dp_gov_map = {
        "1DP" : "1G",
        "6DP" : "6G",
        "7DP" : "7G",
        "8DP" : "8G",
    }
    extra_context = extra_context or {} 

    country_calcs = None
    countries = Country.objects.all().order_by("country")
    if indicator in dp_gov_map:
        gov_indicator = dp_gov_map[indicator]
        country_calcs = [(c, calc_country_ratings(c)[gov_indicator]) for c in countries]
    
    agencies = []
    for agency in Agency.objects.all():
        agency_values = []
        for country in countries:
            if country in agency.countries:
                indicators = calc_agency_country_indicators(agency, country, positive_funcs)
                ratings = country_agency_indicator_ratings(country, agency)

                base_val, base_year, latest_val, _ = indicators[indicator][0]
                country_abs_values = {
                    "baseline_value" : tbl_float_format(base_val), 
                    "latest_value" : tbl_float_format(latest_val), 
                    "rating" : ratings[indicator],
                    "cellclass" : "",
                } 
            else:
                country_abs_values = {
                    "baseline_value" : "",
                    "latest_value" : "",
                    "rating" : "",
                    "cellclass" : "notactive",
                } 
                
            agency_values.append((country, country_abs_values))
        agency_values = sorted(agency_values, key=lambda x: x[0].country)
        agencies.append((agency, agency_values))

    agencies = sorted(agencies, key=lambda x: x[0].agency)
    extra_context["agencies"] = agencies
    extra_context["countries"] = countries
    extra_context["country_calcs"] = country_calcs
    
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def gbs_table(request, agency_id, template_name="submissions/gbs_table.html", extra_context=None):
    extra_context = extra_context or {} 
    gbsagency = Agency.objects.all_types().get(pk=agency_id)
    agency = get_object_or_404(Agency, agency=gbsagency.agency.replace("GBS", ""))

    extra_context["agency"] = agency
    extra_context["agency_data"] = calc_agency_ratings(agency)
    extra_context["gbs_agency_data"] = calc_agency_ratings(gbsagency)

    return direct_to_template(request, template=template_name, extra_context=extra_context)

def country_table(request, template_name="submissions/country_table.html", extra_context=None):
    extra_context = extra_context or {}
    abs_values = {}
    for country in Country.objects.all().order_by("country"):
        country_abs_values = {}
        country_ratings = calc_country_ratings(country)
        indicators = calc_country_indicators(country, positive_funcs)
        for indicator in indicators:
            tpl = indicators[indicator][0]
            base_val, base_year, latest_val, latest_year = tpl
            rating = country_ratings[indicator]["target"]

            if type(base_val) == str: base_val = base_val.upper()
            if type(latest_val) == str: latest_val = latest_val.upper()
            if indicator == "2Gb":
                # The indicator turns this into 100/0
                # This code turns it back - to much effort
                # to figure out why it does this
                base_val = "Y" if base_val == 100 else "N"
                latest_val = "Y" if latest_val == 100 else "N"
            if indicator == "2Ga":
                base_val1 = base_val[0] if base_val else None
                base_val2 = base_val[1] if base_val else None
                latest_val1 = latest_val[0] if latest_val else None
                latest_val2 = latest_val[1] if latest_val else None

                country_abs_values["2Ga1"] = (
                    tbl_float_format(base_val1), 
                    tbl_float_format(latest_val1), 
                    None,
                    base_year,
                    rating
                ) 
                country_abs_values["2Ga2"] = (
                    tbl_float_format(base_val2), 
                    tbl_float_format(latest_val2), 
                    None,
                    base_year,
                    rating,
                ) 
            else:
                decimal_places = {
                    "5Ga" : 1
                }
                places = decimal_places.get(indicator, 0)
                country_abs_values[indicator] = (
                    tbl_float_format(base_val, places), 
                    tbl_float_format(latest_val, places), 
                    tbl_float_format(perc_change(base_val, latest_val), places),
                    base_year,
                    rating
                ) 
        abs_values[country.country] = country_abs_values
    extra_context["abs_values"] = sorted(abs_values.items())
    extra_context["spm_map"] = gov_spm_map
        
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

def agency_ratings(request, template_name="submissions/agency_ratings.html", extra_context=None):
    extra_context = extra_context or {}
    ratings = []
    data = get_agencies_scorecard_data()
    agencies = Agency.objects.all().order_by("agency")
    for indicator in dp_indicators:
        rating = {}
        for agency in agencies:
            rating[agency] = data[agency][indicator]["target"]
        ratings.append((indicator, rating, spm_map[indicator]))
    
    extra_context["ratings"] = ratings
    extra_context["agencies"] = agencies
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
