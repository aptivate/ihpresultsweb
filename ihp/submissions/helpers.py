import xlrd
from submissions.models import Submission, DPQuestion

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
    institution = sheet.cell(1, 5).value
    version = sheet.cell(2, 5).value
    submission = Submission.objects.create(
        country=country,
        institution=institution,
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
