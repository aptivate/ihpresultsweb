from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^scorecard/agency/$', 'submissions.views.agency_scorecard', {}, 'agency_scorecard'),
    (r'^admin/', include(admin.site.urls)),
)
