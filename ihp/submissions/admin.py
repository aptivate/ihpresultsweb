from django.contrib import admin
from django import forms
from models import Agency, Country, UpdateAgency, Submission, DPQuestion, GovQuestion, AgencyCountries, AgencyTargets, CountryTargets, AgencyWorkingDraft, CountryWorkingDraft, DPScorecardSummary, DPScorecardRatings, Country8DPFix, MDGData

admin.site.register(Agency)
admin.site.register(Country)
admin.site.register(UpdateAgency)

class SubmissionAdmin(admin.ModelAdmin):
    list_filter = ("agency", "country")
    list_display = ("country", "agency", "date_submitted", "completed_by", "job_title")

admin.site.register(Submission, SubmissionAdmin)

class DPQuestionAdmin(admin.ModelAdmin):
    list_filter = ("question_number", "submission")
    list_display = ("question_number", "country", "agency")

    def country(self, question):
        return question.submission.country

    def agency(self, question):
        return question.submission.agency
        
        

admin.site.register(DPQuestion, DPQuestionAdmin)

admin.site.register(GovQuestion)

class AgencyCountriesAdmin(admin.ModelAdmin):
    list_filter = ("agency", "country")

    def country(self, question):
        return question.submission.country

    def agency(self, question):
        return question.submission.agency
        
admin.site.register(AgencyCountries, AgencyCountriesAdmin)
class AgencyTargetsAdmin(admin.ModelAdmin):
    list_filter = ("agency", "indicator")
    list_display = ("agency", "indicator", "tick_criterion_type", "tick_criterion_value", "arrow_criterion_type", "arrow_criterion_value")
admin.site.register(AgencyTargets, AgencyTargetsAdmin)

class CountryTargetsAdmin(admin.ModelAdmin):
    list_filter = ("country", "indicator")
    list_display = ("country", "indicator", "tick_criterion_type", "tick_criterion_value", "arrow_criterion_type", "arrow_criterion_value")
admin.site.register(CountryTargets, CountryTargetsAdmin)

admin.site.register(AgencyWorkingDraft)
admin.site.register(CountryWorkingDraft)
admin.site.register(DPScorecardSummary)
admin.site.register(DPScorecardRatings)

class Country8DPFixAdmin(admin.ModelAdmin):
    list_filter = ("agency", "country")
    list_display = ("agency", "country", "baseline_progress", "latest_progress")

admin.site.register(Country8DPFix, Country8DPFixAdmin)

class MDGDataAdminForm(forms.ModelForm):
    class Meta:
        model = MDGData

    baseline_year = forms.ChoiceField(choices=[(x, x) for x in range(1990, 2011)]) 
    latest_year = forms.ChoiceField(choices=[(x, x) for x in range(1990, 2011)]) 
    arrow = forms.ChoiceField(choices=[(None, "")] + [(x, x) for x in ["upgreen", "upred", "downgreen", "downred", "equals"]]) 

class MDGDataAdmin(admin.ModelAdmin):
    list_filter = ("country", "mdg_target")
    list_display = ("country", "mdg_target", "baseline_year", "baseline_value", "latest_year", "latest_value", "arrow")
    form = MDGDataAdminForm
admin.site.register(MDGData, MDGDataAdmin)
