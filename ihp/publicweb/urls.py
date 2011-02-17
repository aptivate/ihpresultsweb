from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list
# from publicweb.models import Resource, Tool

from ihp.publicweb.views import *

urlpatterns = patterns('ihp.publicweb.views',
        url(r'^scorecard/agency/(?P<agency_name>[-\w ]+)/$',
            agency_scorecard_page,
            name='public-agency-scorecard'),
        url(r'^scorecard/country/(?P<country_name>[-\w ]+)/$',
            country_scorecard_page,
            name='public-country-scorecard'),
    )