from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from submissions.models import Agency, DPScorecardSummary
from views import calc_agency_comments
from target import calc_agency_targets
import indicators

def dp_summary(request, agency_id):

    agency = get_object_or_404(Agency, id=agency_id)
    summary, _ = DPScorecardSummary.objects.get_or_create(agency=agency)

    if request.method == "GET":
        agency_data = calc_agency_targets(agency)

        comments = {}
        for indicator in indicators.dp_indicators:
            comments[indicator] = calc_agency_comments(indicator, agency_data)

        comments["summary1"] = summary.erb1
        comments["summary2"] = summary.erb2
        comments["summary3"] = summary.erb3
        comments["summary4"] = summary.erb4
        comments["summary5"] = summary.erb5
        comments["summary6"] = summary.erb6
        comments["summary7"] = summary.erb7
        comments["summary8"] = summary.erb8

        return HttpResponse(simplejson.dumps(comments))
    elif request.method == "POST":
        summary.erb1 = request.POST["summary1"]
        summary.erb2 = request.POST["summary2"]
        summary.erb3 = request.POST["summary3"]
        summary.erb4 = request.POST["summary4"]
        summary.erb5 = request.POST["summary5"]
        summary.erb6 = request.POST["summary6"]
        summary.erb7 = request.POST["summary7"]
        summary.erb8 = request.POST["summary8"]
        print request.POST
        summary.save()

        return HttpResponse("OK")
    
