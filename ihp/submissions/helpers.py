import sys
import xlrd
import urllib2
import json
from submissions.models import Submission, DPQuestion, AgencyCountries, AgencyTargets, Agency, Country, GovQuestion, CountryTargets, MDGData

"""
Functions used for parsing xls submissions - this code will be deprecated by March 2011 as there will no longer be a need to submit instruments via email.
"""

def parse_mdg_file(filename):
    year = lambda x : int(x) if x else x
    empty = lambda x : x if x else None

    def create_mdg_datum(country, target, row, first_col):
        return MDGData.objects.create(
            country=country,
            mdg_target=target,
            baseline_year=empty(year(sheet.cell(row, first_col + 5).value)), 
            baseline_value=empty(sheet.cell(row, first_col + 4).value),
            latest_year=empty(year(sheet.cell(row, first_col + 1).value)), 
            latest_value=empty(sheet.cell(row, first_col + 0).value),
            arrow=empty(sheet.cell(row, first_col + 2).value)
        )
        
        
    book = xlrd.open_workbook(filename)
    for sheet in book.sheets():
        if sheet.cell(0, 0).value == "MILLENNIUM DEVELOPMENT GOALS":
            MDGData.objects.all().delete()
            for row in range(sheet.nrows):
                country = sheet.cell(row, 0).value 
                try:
                    country = Country.objects.get(country=country)
                    create_mdg_datum(country, "MDG1", row, 1)
                    create_mdg_datum(country, "MDG2", row, 13)
                    create_mdg_datum(country, "MDG3", row, 19)
                    create_mdg_datum(country, "MDG4", row, 25)
                    create_mdg_datum(country, "MDG5a", row, 31)
                    create_mdg_datum(country, "MDG5b", row, 37)
                    create_mdg_datum(country, "MDG6a", row, 43)
                    create_mdg_datum(country, "MDG6b", row, 49)
                    create_mdg_datum(country, "MDG6c", row, 55)
                    create_mdg_datum(country, "MDG7a", row, 61)
                    create_mdg_datum(country, "MDG7b", row, 67)
                except Country.DoesNotExist:
                    pass

def parse_file(filename):
    book = xlrd.open_workbook(filename)
    for sheet in book.sheets():
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
    if sheet.cell(3, 2).value == "Objectif":
        # French submission
        country = sheet.cell(0, 4).value
        agency = sheet.cell(1, 4).value
        version = sheet.cell(2, 5).value
        completed_by = sheet.cell(0, 8).value
        job = sheet.cell(1, 8).value
    else:
        country = sheet.cell(0, 3).value
        agency = sheet.cell(1, 3).value
        version = sheet.cell(2, 5).value
        completed_by = sheet.cell(0, 8).value
        job = sheet.cell(1, 8).value

    agency = Agency.objects.all_types().get(agency=agency)
    country = Country.objects.get(country=country)

    DPQuestion.objects.filter(
        submission__country=country,
        submission__agency=agency,
        submission__type="DP"
    ).delete()

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
        completed_by=completed_by,
        job_title=job
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

    if sheet.cell(3, 2).value == "Objectif":
        # French submission
        country = sheet.cell(0, 4).value
        agency = sheet.cell(1, 4).value
        version = sheet.cell(2, 5).value
        completed_by = sheet.cell(0, 8).value
        job = sheet.cell(1, 8).value
    else:
        country = sheet.cell(0, 3).value
        agency = sheet.cell(1, 3).value
        version = sheet.cell(2, 5).value
        completed_by = sheet.cell(0, 8).value
        job = sheet.cell(1, 8).value
    # There is a spelling mistake in the instrument
    # which i am lazily correcting here
    agency = agency.replace("Goverment", "Government")
    if not agency.startswith("Government"):
        agency = "Government of " + agency

    agency = Agency.objects.all_types().get(agency=agency)
    country = Country.objects.get(country=country)

    GovQuestion.objects.filter(
        submission__country=country,
        submission__agency=agency,
        submission__type="Gov"
    ).delete()

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
        completed_by=completed_by,
        job_title=job
    )

    for row in range(4, sheet.nrows):
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
