from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^scorecard/agency/$', 'submissions.views.agency_scorecard', {}, 'agency_scorecard'),
    (r'^scorecard/agency/csv/$', 'submissions.views.agency_scorecard', {"template_name" : "submissions/agency_scorecard_csv.html"}, 'agency_scorecard'),
    (r'^scorecard/agency/questionnaires/$', 'submissions.views.dp_questionnaire', {}, 'agency_questionnaire'),
    (r'^scorecard/agency/questionnaires/cols/$', 'submissions.views.dp_questionnaire', {"template_name" : "submissions/dp_questionnaire_cols.html"}, 'agency_questionnaire_cols'),
    (r'^scorecard/country/csv/$', 'submissions.views.country_scorecard', {}, 'country_scorecard'),
    (r'^scorecard/country/questionnaires/$', 'submissions.views.gov_questionnaire', {}, 'gov_questionnaire'),
    (r'^admin/', include(admin.site.urls)),
)
