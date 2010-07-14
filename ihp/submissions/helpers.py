import xlrd
import urllib2
import json
from submissions.models import Submission, DPQuestion, AgencyCountries, Targets

def parse_file(filename):
    book = xlrd.open_workbook(filename)
    for sheet in book.sheets():
        if sheet.name == "DPs":
            parse_dp(sheet)
        else:
            print >> sys.stderr, "Unknown sheet: %s" % sheet.name

def unfloat(val):
    if type(val) == float:
        return str(int(val))
    return val
    
def parse_dp(sheet):

    country = sheet.cell(0, 5).value
    agency = sheet.cell(1, 5).value
    version = sheet.cell(2, 5).value

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

    for row in range(5, sheet.nrows):
        DPQuestion.objects.create(
           submission=submission,
           question_number=unfloat(sheet.cell(row, 3).value),
           baseline_year=unfloat(sheet.cell(row, 5).value),
           baseline_value=unfloat(sheet.cell(row, 6).value),
           latest_year=unfloat(sheet.cell(row, 7).value),
           latest_value=unfloat(sheet.cell(row, 8).value),
           comments=sheet.cell(row, 11).value,  
        )

#agency_country_url = "https://ihp.dabbledb.com/publish/sarpam/e955563b-618c-4c9a-a131-8ed69356e570/agencycountries.jsonp"
def load_agency_countries(filename=None):
    #fp = urllib2.urlopen(agency_country_url)
    fp = open(filename)
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
        for country in countries:
           AgencyCountries.objects.create(agency=datum["Name"], country=country)  
    return agencies

def load_agency_targets(filename=None):
    fp = open(filename)
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
    
    Targets.objects.all().delete()
    for datum in data:
        Targets.objects.create(
            indicator=datum["Indicator"],
            agency=datum["Agency"],
            tick_criterion_type=datum["Tick Criterion Type"],
            tick_criterion_value=datum["Tick Criterion Value"],
            arrow_criterion_type=datum["Arrow Criterion Type"],
            arrow_criterion_value=datum["Arrow Criterion Value"],
        )
        

