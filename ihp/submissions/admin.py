from django.contrib import admin
from models import Agency, Country, UpdateAgency, Submission, DPQuestion, GovQuestion, AgencyCountries, AgencyTargets, CountryTargets, AgencyWorkingDraft, CountryWorkingDraft, DPScorecardSummary, DPScorecardRatings, Country8DPFix

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
admin.site.register(AgencyTargets)
admin.site.register(CountryTargets)
admin.site.register(AgencyWorkingDraft)
admin.site.register(CountryWorkingDraft)
admin.site.register(DPScorecardSummary)
admin.site.register(DPScorecardRatings)

class Country8DPFixAdmin(admin.ModelAdmin):
    list_filter = ("agency", "country")
    list_display = ("agency", "country", "baseline_progress", "latest_progress")

admin.site.register(Country8DPFix, Country8DPFixAdmin)
