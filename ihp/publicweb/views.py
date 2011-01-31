from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def agency_scorecard_page(request, agency_name):
    return render_to_response('agency_scorecard.html',
        RequestContext(request, {'agency_name': agency_name}))
