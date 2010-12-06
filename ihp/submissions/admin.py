from django.contrib import admin
from models import Agency, Country, UpdateAgency, Submission, DPQuestion, GovQuestion, AgencyCountries, AgencyTargets, CountryTargets, AgencyWorkingDraft, CountryWorkingDraft, DPScorecardSummary, DPScorecardRatings, Country8DPFix

admin.site.register(Agency)
admin.site.register(Country)
admin.site.register(UpdateAgency)
admin.site.register(Submission)
admin.site.register(DPQuestion)
admin.site.register(GovQuestion)
admin.site.register(AgencyCountries)
admin.site.register(AgencyTargets)
admin.site.register(CountryTargets)
admin.site.register(AgencyWorkingDraft)
admin.site.register(CountryWorkingDraft)
admin.site.register(DPScorecardSummary)
admin.site.register(DPScorecardRatings)

class Country8DPFixAdmin(admin.ModelAdmin):
    list_filter = ("agency", "country")

admin.site.register(Country8DPFix, Country8DPFixAdmin)
