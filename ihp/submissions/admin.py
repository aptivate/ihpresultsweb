from django.contrib import admin
from django import forms
from models import *


class AgencyAdmin(admin.ModelAdmin):
    def queryset(self, request):
        return Agency.objects.all_types()

    list_filter = ("type",)
    list_display = ("agency", "type")

admin.site.register(Agency, AgencyAdmin)
admin.site.register(Country)

class SubmissionAdmin(admin.ModelAdmin):
    list_filter = ("agency", "country")
    list_display = ("country", "agency", "date_submitted", "completed_by", "job_title")

admin.site.register(Submission, SubmissionAdmin)

class DPQuestionAdmin(admin.ModelAdmin):
    list_filter = ("question_number", "submission")
    list_display = ("question_number", "country", "agency", "base_val", "cur_val")
    search_fields = ("submission__country__country", "submission__agency__agency")

    def country(self, question):
        return question.submission.country

    def agency(self, question):
        return question.submission.agency
        
        

admin.site.register(DPQuestion, DPQuestionAdmin)

class GovQuestionAdmin(admin.ModelAdmin):
    list_filter = ("question_number", "submission")
    list_display = ("question_number", "country")

    def country(self, question):
        return question.submission.country

admin.site.register(GovQuestion, GovQuestionAdmin)

class AgencyCountriesAdmin(admin.ModelAdmin):
    list_filter = ("agency", "country")
    list_display = ("agency", "country")

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

class AgencyWorkingDraftAdmin(admin.ModelAdmin):
    list_display = ("agency", "is_draft")
admin.site.register(AgencyWorkingDraft, AgencyWorkingDraftAdmin)

class CountryWorkingDraftAdmin(admin.ModelAdmin):
    list_display = ("country", "is_draft")
admin.site.register(CountryWorkingDraft, CountryWorkingDraftAdmin)
admin.site.register(DPScorecardSummary)

class DPScorecardRatingsAdmin(admin.ModelAdmin):
    list_display = ("agency", "r1" , "r2a", "r2b", "r2c", "r3", "r4", "r5a", "r5b", "r5c", "r6", "r7", "r8")
admin.site.register(DPScorecardRatings, DPScorecardRatingsAdmin)

class GovScorecardRatingsAdmin(admin.ModelAdmin):
    list_display = ("country", "r1" , "r2a", "r2b", "r3", "r4", "r5a", "r5b", "r6", "r7", "r8")

admin.site.register(GovScorecardRatings, GovScorecardRatingsAdmin)
admin.site.register(CountryScorecardOverrideComments)

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

admin.site.register(NotApplicable)

class CountryExclusionAdmin(admin.ModelAdmin):
    list_filter = ("question_number", "country" )
    list_display = ("question_number", "country", "baseline_applicable", "latest_applicable")

admin.site.register(CountryExclusion, CountryExclusionAdmin)
admin.site.register(Language)
