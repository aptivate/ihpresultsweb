from collections import defaultdict
from django.conf.urls.defaults import *
from django.views.static import serve
from django.conf import settings

from django.views.generic.simple import direct_to_template
from django.contrib import admin
from submissions.models import Agency, Country

admin.autodiscover()


agency_ratio_titles = {
    "2DPa" : "Increase in %(agency_name)s's aid flows to the health sector not reported on goverment's budget (2DPa)",
    "2DPb" : "%% of technical assistance disbursed through programmes (WB, Target: 50%%)",
    "2DPc" : "%% of aid flows provided in the context of programme base approaches (Target: 66%%)",
    "3DP"  : "%% of health sector funding provided through multi-year commitments",
    "4DP"  : "Increase in %(agency_name)s's health sector aid not disbursed within the year for which it was scheduled (4DP)",
    "5DPa" : "%% change in health sector aid to the public sector not using partner countries' procurement systems",
    "5DPb" : "Increase in %(agency_name)s's health sector aid to the public sector not using partner countries' PFM systems (5DPb)",
    "5DPc" : "Reduction in %(agency_name)s's stock of parallel project implementation (PIUs) units (5DPc)",
}

agency_abs_titles = dict(agency_ratio_titles)
agency_abs_titles["5DPa"] = "%% of health sector aid to the public sector not using partner countries' procurement systems"

agency_yaxis = {
    "2DPa" : "%% increase in funds not reported on government's budget",
    "2DPb" : "%% of programme-based technical assistance",
    "2DPc" : "%% of aid flows",
    "3DP"  : "%% of health sector funding provided through multi-year commitments",
    "4DP"  : "%% increase in health sector aid not disbursed within the year for which it was scheduled",
    "5DPa" : "%% change in health sector aid to the public sector not using partner countries' procurement systems",
    "5DPb" : "%% increase of health sector aid to the public sector not using partner countries' PFM systems",
    "5DPc" : "%% reduction in stock of parallel project implementation (PIUs) units",
}

agency_xaxis = "IHP+ Country"

country_ratio_titles = {
    "2DPa" : "Increase in %(country_name)s's aid flows to the health sector not reported on goverment's budget (2DPa)",
    "2DPb" : "%% of technical assistance disbursed through programmes (WB, Target: 50%%)",
    "2DPc" : "%% of aid flows provided in the context of programme base approaches (Target: 66%%)",
    "3DP"  : "%% of health sector funding provided through multi-year commitments",
    "4DP"  : "Increase in %(country_name)s's health sector aid not disbursed within the year for which it was scheduled (4DP)",
    "5DPa" : "%% change in health sector aid to the public sector not using partner countries' procurement systems",
    "5DPb" : "Increase in %(country_name)s's health sector aid to the public sector not using partner countries' PFM systems (5DPb)",
    "5DPc" : "Reduction in %(country_name)s's stock of parallel project implementation (PIUs) units (5DPc)",
}

country_abs_titles = dict(country_ratio_titles)
country_abs_titles["5DPa"] = "%% of health sector aid to the public sector not using partner countries' procurement systems"
country_yaxis = agency_yaxis
country_xaxis = "IHP+ Agency"

urlpatterns = patterns('',

    (r'^$', direct_to_template, {"template" : "home.html", "extra_context" : {
        "agencies" : Agency.objects.filter(type="Agency"),
        "gbsagencies" : Agency.objects.get_by_type("GBS"),
        "countries" : Country.objects.all(),
    }}, "home"),

    # New csv views
    (r'^scorecard/export/agencies/(?P<language>.+)/$', 'submissions.views.agency_export_lang', {}, 'agency_export_lang'),
    #(r'^scorecard/export/agencies/$', 'submissions.views.agency_export', {}, 'agency_export_english'),
    (r'^scorecard/export/countries/(?P<language>.+)/$', 'submissions.views.country_export', {}, 'country_export'),

    # Edit views
    (r'^scorecard/edit/agencies/summary/$', 'submissions.views.dp_summary_edit', {}, 'dp_summary_edit'),
    (r'^scorecard/edit/agencies/ratings/$', 'submissions.views.dp_ratings_edit', {}, 'dp_ratings_edit'),
    (r'^scorecard/edit/countries/ratings/$', 'submissions.views.gov_ratings_edit', {}, 'gov_ratings_edit'),
    (r'^scorecard/edit/countries/general/$', 'submissions.views.country_scorecard_ratings_edit', {}, 'country_scorecard_ratings_edit'),

    # Api views
    (r'^api/dp_summary/(?P<agency_id>\d+)/$', 'submissions.api.dp_summary', {}, 'api_dp_summary'),
    (r'^api/dp_ratings/(?P<agency_id>\d+)/$', 'submissions.api.dp_ratings', {}, 'api_dp_ratings'),
    (r'^api/gov_ratings/(?P<country_id>\d+)/$', 'submissions.api.gov_ratings', {}, 'api_gov_ratings'),
    (r'^api/country_scorecard/(?P<country_id>\d+)/$', 'submissions.api.country_scorecard', {}, 'api_country_scorecard'),

    # Graph Views
    (r"^agencies/graphs/highlevel/$", "submissions.graphs.highlevelgraphs", {}, "highlevelgraphs"),
    (r"^agencies/graphs/projection/$", "submissions.graphs.projectiongraphs", {}, "projectiongraphs"),
    (r"^agencies/graphs/additional/$", "submissions.graphs.additional_graphs", {}, "additionalgraphs"),

    (r"^agencies/(?P<agency_name>[a-zA-Z\s]+)/graphs/$", "submissions.graphs.agencygraphs", {
        "titles" : agency_ratio_titles,
        "yaxes" : agency_yaxis,
        "xaxis" : agency_xaxis,
    }, "agencygraphs"),

    (r"^agencies/(?P<agency_name>[a-zA-Z\s]+)/graphs/absolute$", "submissions.graphs.agencygraphs", {
        "template_name" : "submissions/agencygraphs_absolute.html",
        "titles" : agency_abs_titles,
        "yaxes" : agency_yaxis,
        "xaxis" : agency_xaxis,
    }, "agencygraphs_absolute"),

    (r"^agencies/graphs/by_country/(?P<country_name>[a-zA-Z\s]+)/ratio_graph/$", "submissions.graphs.countrygraphs", {
        "titles" : country_ratio_titles,
        "yaxes" : country_yaxis,
        "xaxis" : country_xaxis,
    }, "countrygraphs"),

    (r"^agencies/graphs/by_country/(?P<country_name>[a-zA-Z\s]+)/absolute_graph/$", "submissions.graphs.countrygraphs", {
        "template_name" : "submissions/countrygraphs_absolute.html",
        "titles" : country_ratio_titles,
        "yaxes" : country_yaxis,
        "xaxis" : country_xaxis,
    }, "countrygraphs_absolute"),

    (r"^countries/graphs/$", "submissions.graphs.government_graphs", {
        "template_name" : "submissions/main_base.html",
        "extra_context" : {
            "content_file" : "submissions/country_graphs_by_indicator.html"
        }
    }, "government_graphs"),

    # Table Views
    (r'^agencies/tables/by_country/(?P<country_id>\d+)/$', 'submissions.views.agency_table_by_country', {
        "template_name" : "submissions/main_base.html",
        "extra_context" : {
            "content_file" : "submissions/agency_table.html"
        }
    }, 'agency_table_by_country'),

    (r'^agencies/agency/tables/(?P<agency_id>\d+)/$', 'submissions.views.agency_table_by_agency', {
        "template_name" : "submissions/main_base.html",
        "extra_context" : {
            "content_file" : "submissions/agency_table.html"
        }
    }, 'agency_table_by_agency'),

    (r'^agencies/tables/by_indicator/(?P<indicator>.+)/$', 'submissions.views.agency_table_by_indicator', {
        "template_name" : "submissions/main_base.html",
        "extra_context" : {
            "content_file" : "submissions/agency_table_by_indicator.html"
        }
    }, 'agency_table_by_indicator'),

    (r'^agencies/agency/gbs/(?P<agency_id>.+)/$', 'submissions.views.gbs_table', {
        "template_name" : "submissions/main_base.html",
        "extra_context" : {
            "content_file" : "submissions/gbs_table.html"
        }
    }, 'gbs_table'),

    (r'^agencies/alternative_baselines/$', 'submissions.views.agency_alternative_baselines', {
        "template_name" : "submissions/main_base.html",
        "extra_context" : {
            "content_file" : "submissions/agency_alternative_baselines.html"
        }
    }, 'agency_alternative_baselines'),

    (r'^countries/tables/$', 'submissions.views.country_table', {
        "template_name" : "submissions/main_base.html",
        "extra_context" : {
            "content_file" : "submissions/country_table.html"
        }
    }, 'country_table'),

    (r'^countries/tables/matrix$', 'submissions.views.country_table', {
        "template_name" : "submissions/main_base.html",
        "extra_context" : {
            "content_file" : "submissions/country_matrix.html"
        }
    }, 'country_matrix'),

    # Data Tables Views
    (r'^datatables/$', direct_to_template, {"template" : "submissions/datatables.html", "extra_context" : {
        "agencies" : Agency.objects.filter(type="Agency"),
        "countries" : Country.objects.all(),
    }}, "datatables"),

    (r'^datatables/tables/agency/by_country/(?P<country_id>\d+)/$', 'submissions.views.agency_table_by_country', {
        "template_name" : "submissions/datatables_base.html",
        "extra_context" : {
            "content_file" : "submissions/agency_table.html"
        }
    }, 'datatables_agency_table_by_country'),

    (r'^datatables/tables/agency/by_agency/(?P<agency_id>\d+)/$', 'submissions.views.agency_table_by_agency', {
        "template_name" : "submissions/datatables_base.html",
        "extra_context" : {
            "content_file" : "submissions/agency_table.html"
        }
    }, 'datatables_agency_table_by_agency'),

    (r'^datatables/tables/country/matrix$', 'submissions.views.country_table', {
        "template_name" : "submissions/datatables_base.html",
        "extra_context" : {
            "content_file" : "submissions/country_matrix.html"
        }
    }, 'datatables_country_matrix'),

    (r'^scorecard/tables/agency_country_ratings/$', 'submissions.views.agency_country_ratings', {}, 'agency_country_ratings'),
    (r'^datatables/tables/agency_ratings/$', 'submissions.views.agency_ratings', {}, 'agency_ratings'),


    # Old views
    (r'^scorecard/agency/questionnaires/$', 'submissions.views.dp_questionnaire', {}, 'agency_questionnaire'),
    (r'^scorecard/agency/questionnaires/cols/$', 'submissions.views.dp_questionnaire', {"template_name" : "submissions/dp_questionnaire_cols.html"}, 'agency_questionnaire_cols'),
    (r'^scorecard/country/questionnaires/$', 'submissions.views.gov_questionnaire', {}, 'gov_questionnaire'),
    
    # Public website views
    (r'^public/', include('ihp.publicweb.urls')),

    (r'^admin/', include(admin.site.urls)),

)

_media_url = settings.MEDIA_URL
if _media_url.startswith('/'):
    _media_url = _media_url[1:]
urlpatterns += patterns('',
    (r'^%s(?P<path>.*)$' % _media_url, serve,
        {'document_root' : settings.MEDIA_ROOT}, 'ihp-media'))
del(_media_url, serve)
