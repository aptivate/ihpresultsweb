import sys
import xlrd
import urllib2
import json
from submissions.models import Submission, DPQuestion, AgencyCountries, AgencyTargets, Agency, Country, GovQuestion, CountryTargets

def parse_file(filename):
    book = xlrd.open_workbook(filename)
    for sheet in book.sheets():
        #if sheet.name == "DPs":
        if sheet.name == "Survey Tool":
            if sheet.cell(4, 0).value == "1DP":
                parse_dp(sheet)
            elif sheet.cell(4, 0).value == "1G":
                parse_gov(sheet)
        else:
            print >> sys.stderr, "Unknown sheet: %s" % sheet.name

def unfloat(val):
    if type(val) == float:
        return str(int(val))
    return val

def parse_dp(sheet):

    country = sheet.cell(0, 3).value
    agency = sheet.cell(1, 3).value
    version = sheet.cell(2, 5).value
    completed_by = sheet.cell(0, 8).value
    job = sheet.cell(1, 8).value

    agency = Agency.objects.get(agency=agency)
    country = Country.objects.get(country=country)

    Submission.objects.filter(
        country=country,
        agency=agency,
        type="DP"
    ).delete()

    submission = Submission.objects.create(
        country=country,
        agency=agency,
        docversion=version,
        type="DP",
    )

    for row in range(4, sheet.nrows):
        DPQuestion.objects.create(
           submission=submission,
           question_number=unfloat(sheet.cell(row, 3).value),
           baseline_year=unfloat(sheet.cell(row, 5).value),
           baseline_value=sheet.cell(row, 6).value,
           latest_year=unfloat(sheet.cell(row, 7).value),
           latest_value=sheet.cell(row, 8).value,
           comments=sheet.cell(row, 12).value,  
        )

def parse_gov(sheet):

    country = sheet.cell(0, 3).value
    agency = sheet.cell(1, 3).value
    version = sheet.cell(2, 5).value
    completed_by = sheet.cell(0, 8).value
    job = sheet.cell(1, 8).value

    print country, agency, version, completed_by, job

    country = Country.objects.get(country=country)

    Submission.objects.filter(
        country=country,
        agency=agency,
        type="Gov"
    ).delete()

    submission = Submission.objects.create(
        country=country,
        agency=agency,
        docversion=version,
        type="Gov",
    )

    for row in range(5, sheet.nrows):
        base_val = sheet.cell(row, 6).value
        cur_val = sheet.cell(row, 8).value
        base_val = base_val if base_val != "" else None
        cur_val = cur_val if cur_val != "" else None

        GovQuestion.objects.create(
           submission=submission,
           question_number=unfloat(sheet.cell(row, 3).value),
           baseline_year=unfloat(sheet.cell(row, 5).value),
           baseline_value=base_val,
           latest_year=unfloat(sheet.cell(row, 7).value),
           latest_value=cur_val,
           comments=sheet.cell(row, 12).value,  
        )

agency_country_url = "https://ihp.dabbledb.com/publish/sarpam/e955563b-618c-4c9a-a131-8ed69356e570/agencycountries.jsonp"
def load_agency_countries(filename=None):
    if filename:
        fp = open(filename)
    else:
        fp = urllib2.urlopen(agency_country_url)
    s = fp.read()
    js = json.loads(s)
    cols = {}
    data = []
    for key in js["fields"]:
        cols[key] = js["fields"][key]["name"]

    agencies = []
    for entry in js["entries"]:
        datum = {}
        for field in entry["fields"]:
            col = cols[field["field"]]
            if "values" in field:
                countries = []
                for value in field["values"]:
                    countries.append(value["value"])
                datum[col] = countries
            else:
                datum[col] = field["value"]
        agencies.append(datum)
    AgencyCountries.objects.all().delete()
    for datum in agencies:
        countries = datum["Country"]
        (agency, _) = Agency.objects.get_or_create(agency=datum["Name"])
        agency.description = datum["Description"]
        agency.save()
        for country in countries:
            (country, _) = Country.objects.get_or_create(country=country)
            AgencyCountries.objects.create(agency=agency, country=country)  
    return agencies

#agency_targets_url = "https://ihp.dabbledb.com/publish/sarpam/8fefaf12-ad89-4600-beb6-374898c37809/targets.jsonp"
agency_targets_url = "https://ihp.dabbledb.com/publish/sarpam/94c69b3b-b1b1-48a4-8db7-817abed84029/agencytargets.jsonp"

def load_agency_targets(filename=None):
    if filename:
        fp = open(filename)
    else:
        fp = urllib2.urlopen(agency_targets_url)
    js = json.load(fp)
    cols = {}
    data = []

    for key in js["fields"]:
        cols[key] = js["fields"][key]["name"]

    #import pdb; pdb.set_trace();
    for entry in js["entries"]:
        datum = {}
        for field in entry["fields"]:
            key = cols[field["field"]]
            value = field["value"]
            if type(value) == dict:
                value = value["value"]
            datum[key] = value or None
        data.append(datum)
    
    AgencyTargets.objects.all().delete()
    for datum in data:
        if datum["Indicator"] == None:
            continue
        try:
            if datum["Agency"] == None:
                agency = None
            else:
                agency = Agency.objects.get(agency=datum["Agency"])

            AgencyTargets.objects.create(
                indicator=datum["Indicator"],
                agency=agency,
                tick_criterion_type=datum["Tick Criterion Type"],
                tick_criterion_value=datum["Tick Criterion Value"],
                arrow_criterion_type=datum["Arrow Criterion Type"],
                arrow_criterion_value=datum["Arrow Criterion Value"],
            )
        except Agency.DoesNotExist:
            print >> sys.stderr, "Warning - Agency %s does not exist" % datum["Agency"]

def load_dabble_json(url, filename=None):
    if filename:
        fp = open(filename)
    else:
        fp = urllib2.urlopen(government_targets_url)
    js = json.load(fp)
    cols = {}
    data = []

    for key in js["fields"]:
        cols[key] = js["fields"][key]["name"]

    #import pdb; pdb.set_trace();
    for entry in js["entries"]:
        datum = {}
        for field in entry["fields"]:
            key = cols[field["field"]]
            value = field["value"]
            if type(value) == dict:
                value = value["value"]
            datum[key] = value or None
        data.append(datum)
    return data

government_targets_url = "https://ihp.dabbledb.com/publish/sarpam/075101bc-07c0-4fe6-9c92-f9675d171084/governmenttargets.jsonp"
def load_government_targets(filename=None):
    data = load_dabble_json(government_targets_url, filename)
    
    CountryTargets.objects.all().delete()
    for datum in data:
        if datum["Indicator"] == None:
            continue
        try:
            if datum["Country"] == None:
                country = None
            else:
                country = Country.objects.get(country=datum["Country"])

            CountryTargets.objects.create(
                indicator=datum["Indicator"],
                country=country,
                tick_criterion_type=datum["Tick Criterion Type"],
                tick_criterion_value=datum["Tick Criterion Value"],
                arrow_criterion_type=datum["Arrow Criterion Type"],
                arrow_criterion_value=datum["Arrow Criterion Value"],
            )
        except Country.DoesNotExist:
            print >> sys.stderr, "Warning - Country %s does not exist" % datum["Country"]
