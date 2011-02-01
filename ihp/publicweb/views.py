from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import submissions.target
from submissions.models import Submission

class Indicator:
    expected_result = property()
    rating = property()
    overall_progress = property()

def agency_scorecard_page(request, agency_name):
    agency = submissions.models.Agency.objects.get(agency=agency_name)
    ratings = submissions.target.calc_agency_ratings(agency)
    
    context = dict(agency=agency)
    indicators = context['indicators'] = []
    
    for indicator_code, rating in ratings.iteritems():
        i = Indicator()
        
        if indicator_code == "1DP":
            i.expected_result = "Commitments are documented and mutually agreed"
        else:
            i.expected_result = indicator_code
        
        i.rating = rating['target']
        i.overall_progress = rating['commentary']
        indicators.append(i)
        
    p, np = submissions.target.get_country_progress(agency)
    context['progress_countries'] = p.values()
    context['no_progress_countries'] = np.values()
    
    return render_to_response('agency_scorecard.html',
        RequestContext(request, context))

def country_scorecard_page(request, country_name):
    country = submissions.models.Country.objects.get(country=country_name)
    ratings = submissions.target.calc_country_ratings(country)
    
    context = dict(country=country)
    indicators = context['indicators'] = []
    
    for indicator_code, rating in ratings.iteritems():
        i = Indicator()
        
        if indicator_code == "1DP":
            i.expected_result = "Commitments are documented and mutually agreed"
        else:
            i.expected_result = indicator_code
        
        i.rating = rating['target']
        i.overall_progress = rating['commentary']
        indicators.append(i)
        
    p, np = submissions.target.get_agency_progress(country)
    context['progress_agencies'] = p.values()
    context['no_progress_agencies'] = np.values()
    
    return render_to_response('country_scorecard.html',
        RequestContext(request, context))
