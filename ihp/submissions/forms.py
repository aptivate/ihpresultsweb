from django import forms
from django.utils.functional import curry

from submissions.models import Agency, Country, Language
from submissions.utils import classmaker
from target import Rating


RatingsField = curry(forms.ChoiceField, choices=[
    (val, val) 
    for val in ["", Rating.TICK, Rating.ARROW, Rating.CROSS, Rating.QUESTION, Rating.NONE]
])

TextField = curry(forms.CharField, widget=forms.Textarea)

class AgencyForm(forms.Form):
    agency = forms.ChoiceField(choices=[("", "")] + [
        (a.id, a.agency) 
        for a in Agency.objects.filter(type="Agency")
    ])

    class Media:
        js = ("js/jquery-1.4.4.min.js ", "js/jquery.loading.1.6.4.min.js", )
        css = {
            "all": ("css/jquery.loading.1.6.css", "css/dp_summary.css")
        }

class CountryForm(forms.Form):
    country = forms.ChoiceField(choices=[("", "")] + [
        (c.id, c.country) 
        for c in Country.objects.all()
    ])

    class Media:
        js = ("js/jquery-1.4.4.min.js ", "js/jquery.loading.1.6.4.min.js", )
        css = {
            "all": ("css/jquery.loading.1.6.css", "css/dp_summary.css")
        }

class DPSummaryForm(AgencyForm):

    text1 = TextField(label="1DP Comments")
    summary1 = TextField(label="1DP Summary")

    text2a = TextField(label="2DPa Comments")
    text2b = TextField(label="2DPb Comments")
    text2c = TextField(label="2DPc Comments")
    summary2 = TextField(label="2DP Summary")

    text3 = TextField(label="3DP Comments")
    summary3 = TextField(label="3DP Summary")

    text4 = TextField(label="4DP Comments")
    summary4 = TextField(label="4DP Summary")

    text5a = TextField(label="5DPa Comments")
    text5b = TextField(label="5DPb Comments")
    text5c = TextField(label="5DPc Comments")
    summary5 = TextField(label="5DP Summary")

    text6 = TextField(label="6DP Comments")
    summary6 = TextField(label="6DP Summary")

    text7 = TextField(label="7DP Comments")
    summary7 = TextField(label="7DP Summary")

    text8 = TextField(label="8DP Comments")
    summary8 = TextField(label="8DP Summary")

    class Media:
        js = ("js/dpsummaryform.js", )

class DPRatingsForm(AgencyForm):

    r1 = RatingsField(label="1DP Rating", required=False)
    er1 = TextField(label="1DP Progress Text")

    r2a = RatingsField(label="2DPa Rating", required=False)
    er2a = TextField(label="2DPa Progress Text")
    r2b = RatingsField(label="2DPb Rating", required=False)
    er2b = TextField(label="2DPb Progress Text")
    r2c = RatingsField(label="2DPc Rating", required=False)
    er2c = TextField(label="2DPc Progress Text")

    r3 = RatingsField(label="3DP Rating", required=False)
    er3 = TextField(label="3DP Progress Text")

    r4 = RatingsField(label="4DP Rating", required=False)
    er4 = TextField(label="4DP Progress Text")

    r5a = RatingsField(label="5DPa Rating", required=False)
    er5a = TextField(label="5DPa Progress Text")
    r5b = RatingsField(label="5DPb Rating", required=False)
    er5b = TextField(label="5DPb Progress Text")
    r5c = RatingsField(label="5DPc Rating", required=False)
    er5c = TextField(label="5DPc Progress Text")

    r6 = RatingsField(label="6DP Rating", required=False)
    er6 = TextField(label="6DP Progress Text")

    r7 = RatingsField(label="7DP Rating", required=False)
    er7 = TextField(label="7DP Progress Text")

    r8 = RatingsField(label="8DP Rating", required=False)
    er8 = TextField(label="8DP Progress Text")

    class Media:
        js = ("js/dpratingsform.js", )

class GovRatingsForm(CountryForm):

    r1 = RatingsField(label="1G Rating", required=False)
    er1_en = TextField(label="1G Progress Text (English)")
    er1_fr = TextField(label="1G Progress Text (French)")

    r2a = RatingsField(label="2Ga Rating", required=False)
    er2a_en = TextField(label="2Ga Progress Text (English)")
    er2a_fr = TextField(label="2Ga Progress Text (French)")
    r2b = RatingsField(label="2Gb Rating", required=False)
    er2b_en = TextField(label="2Gb Progress Text (English)")
    er2b_fr = TextField(label="2Gb Progress Text (French)")

    r3 = RatingsField(label="3G Rating", required=False)
    er3_en = TextField(label="3G Progress Text (English)")
    er3_fr = TextField(label="3G Progress Text (French)")

    r4 = RatingsField(label="4G Rating", required=False)
    er4_en = TextField(label="4G Progress Text (English)")
    er4_fr = TextField(label="4G Progress Text (French)")

    r5a = RatingsField(label="5Ga Rating", required=False)
    er5a_en = TextField(label="5Ga Progress Text (English)")
    er5a_fr = TextField(label="5Ga Progress Text (French)")
    r5b = RatingsField(label="5Gb Rating", required=False)
    er5b_en = TextField(label="5Gb Progress Text (English)")
    er5b_fr = TextField(label="5Gb Progress Text (French)")

    r6 = RatingsField(label="6G Rating", required=False)
    er6_en = TextField(label="6G Progress Text (English)")
    er6_fr = TextField(label="6G Progress Text (French)")

    r7 = RatingsField(label="7G Rating", required=False)
    er7_en = TextField(label="7G Progress Text (English)")
    er7_fr = TextField(label="7G Progress Text (French)")

    r8 = RatingsField(label="8G Rating", required=False)
    er8_en = TextField(label="8G Progress Text (English)")
    er8_fr = TextField(label="8G Progress Text (French)")

    hmis1 = RatingsField(label="HMIS1 Rating", required=False)
    jar1 = RatingsField(label="JAR1 Rating", required=False)
    hsp1 = RatingsField(label="HSP1 Rating", required=False)
    hsp2 = RatingsField(label="HSP2 Rating", required=False)
    hsm1 = RatingsField(label="HSM1 Rating", required=False)
    hsm4 = RatingsField(label="HSM4 Rating", required=False)

    class Media:
        js = ("js/govratingsform.js", )

class CountryScorecardForm(CountryForm):
    rf1 = RatingsField(label="RF1")
    dbr1 = RatingsField(label="DBR1")
    hmis1 = RatingsField(label="HMIS1")
    jar1 = RatingsField(label="JAR1")
    hsp1 = RatingsField(label="HSP1")
    hsp2 = RatingsField(label="HSP2")
    hsm1 = RatingsField(label="HSM1")
    hsm4 = RatingsField(label="HSM4")

    rf1 = RatingsField(label="RF1", required=False)
    rf2_English = TextField(label="RF2 (English)")
    rf2_French = TextField(label="RF2 (French)")
    rf3_English = TextField(label="RF3 (English)")
    rf3_French = TextField(label="RF3 (French)")

    dbr1 = RatingsField(label="DBR1", required=False)
    dbr2_English = TextField(label="DBR2 (English)")
    dbr2_French = TextField(label="DBR2 (French)")

    hmis1 = RatingsField(label="HMIS1", required=False)
    hmis2_English = TextField(label="HMIS2 (English)")
    hmis2_French = TextField(label="HMIS2 (French)")

    jar1 = RatingsField(label="JAR1", required=False)
    jar4_English = TextField(label="JAR4 (English)")
    jar4_French = TextField(label="JAR4 (French)")

    hsp1 = RatingsField(label="HSP1", required=False)
    hsp2 = RatingsField(label="HSP2", required=False)
    hsm1 = RatingsField(label="HSM1", required=False)
    hsm4 = RatingsField(label="HSM4", required=False)

    pfm2_English = TextField(label="PFM2 (English)")
    pfm2_French = TextField(label="PFM2 (French)")
    pr2_English = TextField(label="PR2 (English)")
    pr2_French = TextField(label="PR2 (French)")
    ta2_English = TextField(label="TA2 (English)")
    ta2_French = TextField(label="TA2 (French)")
    pf2_English = TextField(label="PF2 (English)")
    pf2_French = TextField(label="PF2 (French)")
    cd2_English = TextField(label="CD2 (English)")
    cd2_French = TextField(label="CD2 (French)")

    class Media:
        js = ("js/countryscorecardform.js", )

