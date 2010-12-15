from collections import defaultdict
import traceback
from math import fabs
import csv

from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404

from models import Submission, AgencyCountries, Agency, DPQuestion, GovQuestion, Country, MDGData, DPScorecardSummary, AgencyWorkingDraft, CountryWorkingDraft, DPScorecardRatings, GovScorecardRatings
from target import calc_agency_targets, get_country_progress, calc_country_targets, get_agency_progress
from indicators import calc_country_indicators, calc_agency_country_indicators, NA_STR
from forms import DPSummaryForm, DPRatingsForm, GovRatingsForm


def calc_agency_comments(indicator, agency_data):
    old_comments = agency_data[indicator]["comments"]
    comments = []
    for question_number, country, comment in old_comments:
        comments.append("%s %s] %s" % (question_number, country, comment))
    comments = "\n".join([comment for comment in comments if comment])
    return comments

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

def get_country_scorecard_data(country):
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

    submissions = country.submission_set.filter(type="Gov")
    assert submissions.count() == 1

    submission = submissions.all()[0] 

    # Do not process if there are no questions
    if submission.govquestion_set.all().count() == 0: 
        raise Exception("Possible incomplete submission")
    
    country_data = calc_country_targets(country)
    
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
    headings = ["baseline_value", "baseline_year", "latest_value", "latest_year"]
    country_data["indicators"] = {}
    for indicator in indicators:
        country_data["indicators"][indicator] = dict(zip(headings, indicators[indicator][0]))
    country_data["indicators"]["3G"]["hs_budget_gap"] = safe_diff(15, country_data["indicators"]["3G"]["latest_value"])
    country_data["indicators"]["other"] = {}

    # Add agency submissions
    agencies = AgencyCountries.objects.get_country_agencies(country)
    aval = country_data["agencies"] = {}
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
        qvals = country_data["questions"][question.question_number] = {}
        qvals["baseline_year"] = question.baseline_year
        qvals["baseline_value"] = question.baseline_value
        qvals["latest_year"] = question.latest_year
        qvals["latest_value"] = question.latest_value
        qvals["comments"] = question.comments

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

    return country_data

def get_countries_scorecard_data():
    return dict([(country, get_country_scorecard_data(country))
        for country in Country.objects.all()
        if country.submission_set.filter(type="Gov").count() > 0
    ])


def agency_scorecard(request, template_name="submissions/agency_scorecard.html", extra_context=None):
    extra_context = extra_context or {}
    extra_context["targets"] = get_agencies_scorecard_data()

    return direct_to_template(request, template=template_name, extra_context=extra_context)

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

    target_none = lambda target : target if target else "question"

    data = get_agencies_scorecard_data()
    for agency, datum in data.items():
        try:
            ratings, _ = DPScorecardRatings.objects.get_or_create(agency=agency)
            datum["file"] = agency.agency
            datum["agency"] = agency.agency 
            datum["profile"] = agency.description
            for indicator in ["1DP", "2DPa", "2DPb", "2DPc", 
                "3DP", "4DP", "5DPa", "5DPb", "5DPc", "6DP", "7DP", "8DP"]:

                h = indicator.replace("DP", "")
                datum["er%s" % h] = ratings.__dict__["er%s" % h] or datum[indicator]["commentary"]
                datum["r%s" % h] = target_none(ratings.__dict__["r%s" % h] or datum[indicator]["target"])

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

def dp_questionnaire(request, template_name="submissions/dp_questionnaire.html", extra_context=None):

    extra_context = extra_context or {}
    extra_context["questions"] = DPQuestion.objects.filter(
        submission__agency__updateagency__update=True
    ).order_by("submission__agency", "submission__country", "question_number")
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def country_export(request):

    formatter = lambda decimals : lambda x : round(x, decimals) if type(x) == float else x
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
    #fformat_front = lambda x : "%.1f" % x if type(x) == float else x
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

    target_none = lambda target : target if target else "question"

    data = get_countries_scorecard_data()
    for country, datum in data.items():
        try:
            datum["file"] = country.country
            datum["TB2"] = "%s COUNTRY SCORECARD" % country.country.upper()

            datum["CD1"] = target_none(datum["1G"]["target"])
            datum["CD2"] = datum["questions"]["1"]["comments"]
            datum["HSP1"] = target_none(datum["Q2G"]["target"])
            datum["HSP2"] = target_none(datum["Q3G"]["target"])
            datum["HSM1"] = target_none(datum["Q12G"]["target"])
            datum["HSM2"] = fformat_none(datum["questions"]["15"]["latest_value"])
            #datum["HSM3"] = fformat_front(datum["indicators"]["8G"]["latest_value"])
            datum["HSM3"] = target_none(datum["8G"]["target"])
            datum["HSM4"] = ""

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
            datum["PF2"] = datum["questions"]["16"]["comments"]

            datum["PFM1"] = target_none(datum["5Ga"]["target"])
            datum["PFM2"] = datum["questions"]["9"]["comments"]

            datum["PR1"] = target_none(datum["5Gb"]["target"])
            datum["PR2"] = datum["questions"]["10"]["comments"]

            datum["TA1"] = datum["indicators"]["other"]["coordinated_programmes"]
            datum["TA2"] = ""
            for agency in datum["agencies"]:
                aqs = datum["agencies"][agency]
                if "4" in aqs:
                    datum["TA2"] += "%s %s" % (agency, aqs["4"]["comments"].replace("%", "%%"))
                    datum["TA2"] += "\n"

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

            datum["RF1"] = target_none(datum["6G"]["target"])
            datum["RF2"] = fformat_none(datum["questions"]["22"]["latest_value"])
            datum["RF3"] = fformat_none(datum["questions"]["23"]["latest_value"])

            datum["HMIS1"] = target_none(datum["Q21G"]["target"])
            datum["HMIS2"] = datum["questions"]["21"]["comments"]

            datum["JAR1"] = target_none(datum["Q12G"]["target"])
            datum["JAR2"] = ""
            datum["JAR3"] = fformat_front(datum["questions"]["24"]["latest_value"])
            datum["JAR4"] = datum["questions"]["24"]["comments"]
            datum["JAR5"] = datum["questions"]["24"]["comments"]

            datum["DBR1"] = target_none(datum["6G"]["target"])
            datum["DBR2"] = datum["questions"]["11"]["comments"]

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

            datum["ER1a"] = target_none(datum["1G"]["target"])
            datum["ER1b"] = datum["1G"]["commentary"]
            datum["ER2a"] = target_none(datum["2Ga"]["target"])
            datum["ER2b"] = datum["2Ga"]["commentary"]
            datum["ER3a"] = target_none(datum["2Gb"]["target"])
            datum["ER3b"] = datum["2Gb"]["commentary"]
            datum["ER4a"] = target_none(datum["3G"]["target"])
            datum["ER4b"] = datum["3G"]["commentary"]
            datum["ER4c"] = country.country
            datum["ER5a"] = target_none(datum["4G"]["target"])
            datum["ER5b"] = datum["4G"]["commentary"]
            datum["ER6a"] = datum["PFM1"]
            datum["ER6b"] = datum["5Ga"]["commentary"]
            datum["ER7a"] = datum["PR1"]
            datum["ER7b"] = datum["5Gb"]["commentary"]
            datum["ER8a"] = target_none(datum["6G"]["target"])
            datum["ER8b"] = datum["6G"]["commentary"]
            datum["ER9a"] = target_none(datum["7G"]["target"])
            datum["ER9b"] = datum["7G"]["commentary"]
            #datum["ER10a"] = target_none(datum["8G"]["target"])
            datum["ER10a"] = datum["HSM3"]
            datum["ER10b"] = datum["8G"]["commentary"]

            datum["Header"] = country.country

            for i in range(1, 14):
                datum["P%d" % i] = datum["p"].get(i, "pwhite")
                datum["NP%d" % i] = datum["np"].get(i, "npwhite")

            working_draft, _ = CountryWorkingDraft.objects.get_or_create(country=country)
            datum["workingdraft"] = "workingdraft" if working_draft.is_draft else ""

        except Exception, e:
            traceback.print_exc()

    response = HttpResponse(mimetype="text/csv")
    response["Content-Disposition"] = "attachment; filename=country_export.csv"
    writer = csv.writer(response)
    writer.writerow(headers)

    def enc(x):
        if x == None:
            return None
        if type(x) not in [str, unicode]:
            x = unicode(x)
        return x.encode("utf8")
    for agency in data:
        writer.writerow([enc(data[agency].get(header, "")) for header in headers])
    return response

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
    if base_val in none_vals or latest_val in none_vals:
        return None
    if base_val == 0:
        return None
    return (latest_val - base_val) / base_val * 100.0


spm_map = {
    "1DP" : "Proportion of IHP+ countries in which the partner has signed commitment to (or documented support for) the IHP+ Country Compact, or equivalent agreement.",
    "2DPa" : "Percent of aid flows to the health sector that is reported on national health sector budgets.",
    "2DPb" : "Percent of current capacity-development support provided through coordinated programmes consistent with national plans/strategies for the health sector.",
    "2DPc" : "Percent of health sector aid provided as programme based approaches.",
    "3DP" : "Percent of health sector aid provided through multi-year commitments.",
    "4DP" : "Percent of health sector aid disbursements released according to agreed schedules in annual or multi-year frameworks.",
    "5DPa" : "Percent of health sector aid that uses country procurement systems.",
    "5DPb" : "Percent of health sector aid that uses public financial management systems.",
    "5DPc" : "Number of parallel Project Implementation Units (PIUs) per country.",
    "6DP" : "Proportion of countries in which agreed, transparent and monitorable performance assessment frameworks are being used to assess progress in the health sector.",
    "7DP" : "Proportion of countries where mutual assessments have been made of progress implementing commitments in the health sector, including on aid effectiveness.",
    "8DP" : "Evidence of support for Civil Society to be actively represented in health sector policy processes - including Health Sector planning, coordination & review mechanisms.",
}
def country_table(request, country_id, template_name="submissions/agency_table.html", extra_context=None):
    extra_context = extra_context or {} 
    country = get_object_or_404(Country, pk=country_id)

    abs_values = {}
    for agency in country.agencies:
        agency_abs_values = {}
        indicators = calc_agency_country_indicators(agency, country)
        for indicator in indicators:
            base_val, base_year, latest_val, _ = indicators[indicator][0]
            agency_abs_values[indicator] = (base_val, latest_val, perc_change(base_val, latest_val), base_year) 
        abs_values[agency.agency] = agency_abs_values
    extra_context["abs_values"] = sorted(abs_values.items())
    extra_context["spm_map"] = spm_map
    extra_context["institution_name"] = country.country
    
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def agency_table(request, agency_id, template_name="submissions/agency_table.html", extra_context=None):
    extra_context = extra_context or {} 
    agency = get_object_or_404(Agency, pk=agency_id)

    abs_values = {}
    for country in agency.countries:
        country_abs_values = {}
        indicators = calc_agency_country_indicators(agency, country)
        for indicator in indicators:
            base_val, base_year, latest_val, _ = indicators[indicator][0]
            country_abs_values[indicator] = (base_val, latest_val, perc_change(base_val, latest_val), base_year) 
        abs_values[country.country] = country_abs_values
    extra_context["abs_values"] = sorted(abs_values.items())
    extra_context["spm_map"] = spm_map
    extra_context["institution_name"] = agency.agency
    
    return direct_to_template(request, template=template_name, extra_context=extra_context)
