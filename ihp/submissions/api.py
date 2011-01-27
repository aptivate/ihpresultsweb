import re
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from submissions.models import Agency, DPScorecardSummary, DPScorecardRatings, GovScorecardRatings, Country, CountryScorecardOverride, GovQuestion, DPQuestion
from target import calc_agency_ratings, calc_country_ratings
import indicators

def calc_agency_comments(indicator, agency_data):
    old_comments = agency_data[indicator]["comments"]
    comments = []
    for question_number, country, comment in old_comments:
        comments.append("%s %s] %s" % (question_number, country, comment))
    comments = "\n".join([comment for comment in comments if comment])
    return comments

def dp_summary(request, agency_id):

    agency = get_object_or_404(Agency, id=agency_id)
    summary, _ = DPScorecardSummary.objects.get_or_create(agency=agency)
    erbs = range(1, 9)

    if request.method == "GET":
        agency_data = calc_agency_ratings(agency)

        comments = {}
        for indicator in indicators.dp_indicators:
            comments[indicator] = calc_agency_comments(indicator, agency_data)

        for i in erbs:
            comments["summary%d" % i] = getattr(summary, "erb%d" % i)

        return HttpResponse(simplejson.dumps(comments))
    elif request.method == "POST":
        for i in erbs:
            setattr(summary, "erb%d" % i, request.POST["summary%d" % i])
        summary.save()

        return HttpResponse("OK")
    
def dp_ratings(request, agency_id):

    get_comment = lambda indicator : results[indicator]["commentary"]
    strip_indicator = lambda x : x.replace("DP", "")
    try:
        agency = get_object_or_404(Agency, id=agency_id)
        ratings, _ = DPScorecardRatings.objects.get_or_create(agency=agency)
        results = calc_agency_ratings(agency)
        data = {}

        if request.method == "GET":
            agency_data = calc_agency_ratings(agency)

            for indicator in indicators.dp_indicators:
                data[indicator] = calc_agency_comments(indicator, agency_data)
                core_indicator = strip_indicator(indicator)
                data["rating%s" % core_indicator] = getattr(ratings, "r%s" % core_indicator)
                data["progress%s" % core_indicator] = getattr(ratings, "er%s" % core_indicator)
                data["gen%s" % core_indicator] = get_comment(indicator)

            return HttpResponse(simplejson.dumps(data))
        elif request.method == "POST":

            for indicator in indicators.dp_indicators:
                core_indicator = strip_indicator(indicator)
                
                indicator.setattr(ratings, "r%s" % core_indicator, request.POST["r%s" % core_indicator])
                indicator.setattr(ratings, "er%s" % core_indicator, request.POST["er%s" % core_indicator])
            ratings.save()

            results = calc_agency_ratings(agency)

            for indicator in indicators.dp_indicators:
                core_indicator = strip_indicator(indicator)

                data["gen%s" % core_indicator] = results[indicator]["commentary"]

            return HttpResponse(simplejson.dumps(data))
    except:
        import traceback
        traceback.print_exc()
    
def gov_ratings(request, country_id):

    re_indconv = re.compile("(\d+)(\w*)")
    indconv = lambda indicator : "%sG%s" % re_indconv.search(indicator).groups()
    try:
        country = get_object_or_404(Country, id=country_id)
        ratings, _ = GovScorecardRatings.objects.get_or_create(country=country)
        get_comment = lambda indicator : results[indicator]["commentary"]
        data = {}
        indicators = ["1", "2a", "2b", "3", "4", "5a", "5b", "6", "7", "8"]

        if request.method == "GET":
            results = calc_country_ratings(country)
            country_data = results

            
            for indicator in indicators:
                data["rating%s" % indicator] = getattr(ratings, "r%s" % indicator)
                data["progress%s" % indicator] = getattr(ratings, "er%s" % indicator)
                data["gen%s" % indicator] = get_comment(indconv(indicator))

            return HttpResponse(simplejson.dumps(data))
        elif request.method == "POST":

            for indicator in indicators:
                setattr(ratings, "r%s" % indicator, request.POST["r%s" % indicator]) 
                setattr(ratings, "er%s" % indicator, request.POST["er%s" % indicator]) 
                ratings.save()

            results = calc_country_ratings(country)

            for indicator in indicators:
                data["gen%s" % indicator] = get_comment(indconv(indicator))

            return HttpResponse(simplejson.dumps(data))
    except:
        import traceback
        traceback.print_exc()
    
def country_scorecard(request, country_id):

    try:
        country = get_object_or_404(Country, id=country_id)
        ratings, _ = CountryScorecardOverride.objects.get_or_create(country=country)
        data = {}

        if request.method == "GET":
            results = calc_country_ratings(country)
            country_data = results
            data = ratings.__dict__.copy()
            for key in data.keys():
                if key.startswith("_"): del data[key]

            # TODO - this is messy. This default data should be contained elsewhere
            country_questions = GovQuestion.objects.filter(submission__country=country)
            data["rf2"] = data["rf2"] or country_questions.filter(question_number="22")[0].latest_value
            data["rf3"] = data["rf3"] or country_questions.filter(question_number="23")[0].latest_value
            data["dbr2"] = data["dbr2"] or country_questions.filter(question_number="11")[0].comments
            data["hmis2"] = data["hmis2"] or country_questions.filter(question_number="21")[0].comments
            jar4_question = country_questions.filter(question_number="24")[0]
            data["jar4"] = data["jar4"] or "Latest Value: %s\nComment: %s" % (jar4_question.latest_value, jar4_question.comments)
            data["pfm2"] = data["pfm2"] or country_questions.filter(question_number="9")[0].comments
            data["pr2"] = data["pr2"] or country_questions.filter(question_number="10")[0].comments
            data["pf2"] = data["pf2"] or country_questions.filter(question_number="16")[0].comments
            if not data["ta2"]:
                data["ta2"] = ""
                for q in DPQuestion.objects.filter(submission__country=country, question_number="4"):
                    data["ta2"] += q.submission.agency.agency + ": " + q.comments + "\n\n"
                 
            return HttpResponse(simplejson.dumps(data))
        elif request.method == "POST":
            for key in request.POST.keys():
                if key in ratings.__dict__:
                    ratings.__dict__[key] = request.POST[key]

            ratings.save()

            return HttpResponse(simplejson.dumps(data))
    except:
        import traceback
        traceback.print_exc()
    
