from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from submissions.models import Agency

def agency_scorecard_page(request, agency_name):
    agency = Agency.objects.get(agency=agency_name)
    return render_to_response('agency_scorecard.html',
        RequestContext(request, {'agency': agency}))
