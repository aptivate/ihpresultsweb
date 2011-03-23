from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list
# from publicweb.models import Resource, Tool

from ihp.publicweb.views import *

urlpatterns = patterns('ihp.publicweb.views',
        url(r'^scorecard/partner/(?P<agency_name>[-\w ]+)/$',
            agency_scorecard_page,
            name='public-agency-scorecard'),
        url(r'^scorecard/country/(?P<country_name>[-\w ]+)/$',
            country_scorecard_page,
            name='public-country-scorecard'),
        url(r'^table/agency/(?P<agency_name>[-\w ]+)/indicator/(?P<indicator_name>[-\w]+)$',
            agency_spm_countries_table,
            name='agency-spm-countries-table'),
        url(r'^table/country/(?P<country_name>[-\w ]+)$',
            country_spms_table,
            name='country-spms-table'),
        url(r'^table/agency/(?P<agency_name>[-\w ]+)/country/(?P<country_name>[-\w ]+)$',
            agency_country_spms_table,
            name='agency-country-spms-table'),
        url(r'^unicode-test$', unicode_test),
    )