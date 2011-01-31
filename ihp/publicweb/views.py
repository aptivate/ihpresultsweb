from django.http import HttpResponse

def agency_scorecard_page(request, agency_name):
    return HttpResponse('hello %s!' % (agency_name))