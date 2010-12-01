from django import forms
from submissions.models import Agency

class DPSummaryForm(forms.Form):
    agency = forms.ChoiceField(choices=[("", "")] + [
        (a.id, a.agency) 
        for a in Agency.objects.filter(type="Agency")
    ])

    text1 = forms.CharField(widget=forms.Textarea, label="1DP Comments")
    summary1 = forms.CharField(widget=forms.Textarea, label="1DP Summary")

    text2a = forms.CharField(widget=forms.Textarea, label="2DPa Comments")
    text2b = forms.CharField(widget=forms.Textarea, label="2DPb Comments")
    text2c = forms.CharField(widget=forms.Textarea, label="2DPc Comments")
    summary2 = forms.CharField(widget=forms.Textarea, label="2DP Summary")

    text3 = forms.CharField(widget=forms.Textarea, label="3DP Comments")
    summary3 = forms.CharField(widget=forms.Textarea, label="3DP Summary")

    text4 = forms.CharField(widget=forms.Textarea, label="4DP Comments")
    summary4 = forms.CharField(widget=forms.Textarea, label="4DP Summary")

    text5a = forms.CharField(widget=forms.Textarea, label="5DPa Comments")
    text5b = forms.CharField(widget=forms.Textarea, label="5DPb Comments")
    text5c = forms.CharField(widget=forms.Textarea, label="5DPc Comments")
    summary5 = forms.CharField(widget=forms.Textarea, label="5DP Summary")

    text6 = forms.CharField(widget=forms.Textarea, label="6DP Comments")
    summary6 = forms.CharField(widget=forms.Textarea, label="6DP Summary")

    text7 = forms.CharField(widget=forms.Textarea, label="7DP Comments")
    summary7 = forms.CharField(widget=forms.Textarea, label="7DP Summary")

    text8 = forms.CharField(widget=forms.Textarea, label="8DP Comments")
    summary8 = forms.CharField(widget=forms.Textarea, label="8DP Summary")

    class Media:
        js = ("js/jquery-1.4.4.min.js ", "js/dpsummaryform.js", )
        css = {
            "all": ('css/dp_summary.css', )
        }
