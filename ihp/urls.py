from django.conf.urls.defaults import *
from django.views.static import serve
from django.conf import settings

from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^$', direct_to_template, {"template" : "home.html"}, "home"),

    # New csv views
    (r'^scorecard/export/agencies/$', 'submissions.views.agency_export', {}, 'agency_export'),
    (r'^scorecard/export/countries/$', 'submissions.views.country_export', {}, 'country_export'),
    #(r'^api/dp/comments/$', 'submissions.api.dp_comments', {}, 'api_dp_comments')

    # Edit views
    (r'^scorecard/edit/agencies/summary/$', 'submissions.views.dp_summary_edit', {}, 'dp_summary_edit'),

    # Api views
    (r'^api/dp_summary/(?P<agency_id>\d+)/$', 'submissions.api.dp_summary', {}, 'api_dp_summary'),
    

    # Old views
    (r'^scorecard/agency/$', 'submissions.views.agency_scorecard', {}, 'agency_scorecard'),
    (r'^scorecard/agency/csv/$', 'submissions.views.agency_scorecard', {"template_name" : "submissions/agency_scorecard_csv.html"}, 'agency_scorecard'),
    (r'^scorecard/agency/questionnaires/$', 'submissions.views.dp_questionnaire', {}, 'agency_questionnaire'),
    (r'^scorecard/agency/questionnaires/cols/$', 'submissions.views.dp_questionnaire', {"template_name" : "submissions/dp_questionnaire_cols.html"}, 'agency_questionnaire_cols'),
    (r'^scorecard/country/csv/$', 'submissions.views.country_scorecard', {}, 'country_scorecard'),
    (r'^scorecard/country/questionnaires/$', 'submissions.views.gov_questionnaire', {}, 'gov_questionnaire'),

    (r'^admin/', include(admin.site.urls)),

)

_media_url = settings.MEDIA_URL
if _media_url.startswith('/'):
    _media_url = _media_url[1:]
urlpatterns += patterns('', (r'^%s(?P<path>.*)$' % _media_url, serve, {'document_root' : settings.MEDIA_ROOT}))
del(_media_url, serve)
