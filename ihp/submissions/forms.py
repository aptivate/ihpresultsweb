from django import forms
from submissions.models import Agency

class DPSummaryForm(forms.Form):
    agency = forms.ChoiceField(choices=[("", "")] + [
        (a.id, a.agency) 
        for a in Agency.objects.filter(type="Agency")
    ])

    class Media:
        js = ("js/dpsummaryform.js",)
