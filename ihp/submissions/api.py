from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from submissions.models import Agency, DPScorecardSummary, DPScorecardRatings, GovScorecardRatings, Country, CountryScorecardOverride, GovQuestion, DPQuestion
from target import calc_agency_targets, calc_country_targets
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
    
def dp_ratings(request, agency_id):

    get_comment = lambda indicator : results[indicator]["commentary"]
    try:
        agency = get_object_or_404(Agency, id=agency_id)
        ratings, _ = DPScorecardRatings.objects.get_or_create(agency=agency)
        results = calc_agency_targets(agency)
        data = {}

        if request.method == "GET":
            agency_data = calc_agency_targets(agency)

            for indicator in indicators.dp_indicators:
                data[indicator] = calc_agency_comments(indicator, agency_data)

            data["rating1"] = ratings.r1
            data["rating2a"] = ratings.r2a
            data["rating2b"] = ratings.r2b
            data["rating2c"] = ratings.r2c
            data["rating3"] = ratings.r3
            data["rating4"] = ratings.r4
            data["rating5a"] = ratings.r5a
            data["rating5b"] = ratings.r5b
            data["rating5c"] = ratings.r5c
            data["rating6"] = ratings.r6
            data["rating7"] = ratings.r7
            data["rating8"] = ratings.r8
            data["progress1"] = ratings.er1
            data["progress2a"] = ratings.er2a
            data["progress2b"] = ratings.er2b
            data["progress2c"] = ratings.er2c
            data["progress3"] = ratings.er3
            data["progress4"] = ratings.er4
            data["progress5a"] = ratings.er5a
            data["progress5b"] = ratings.er5b
            data["progress5c"] = ratings.er5c
            data["progress6"] = ratings.er6
            data["progress7"] = ratings.er7
            data["progress8"] = ratings.er8

            data["gen1"] = get_comment("1DP")
            data["gen2a"] = get_comment("2DPa")
            data["gen2b"] = get_comment("2DPb")
            data["gen2c"] = get_comment("2DPc")
            data["gen3"] = get_comment("3DP")
            data["gen4"] = get_comment("4DP")
            data["gen5a"] = get_comment("5DPa")
            data["gen5b"] = get_comment("5DPb")
            data["gen5c"] = get_comment("5DPc")
            data["gen6"] = get_comment("6DP")
            data["gen7"] = get_comment("7DP")
            data["gen8"] = get_comment("8DP")

            return HttpResponse(simplejson.dumps(data))
        elif request.method == "POST":
            ratings.r1 = request.POST["r1"]
            ratings.er1 = request.POST["er1"]
            ratings.r2a = request.POST["r2a"]
            ratings.er2a = request.POST["er2a"]
            ratings.r2b = request.POST["r2b"]
            ratings.er2b = request.POST["er2b"]
            ratings.r2c = request.POST["r2c"]
            ratings.er2c = request.POST["er2c"]
            ratings.r3 = request.POST["r3"]
            ratings.er3 = request.POST["er3"]
            ratings.r4 = request.POST["r4"]
            ratings.er4 = request.POST["er4"]
            ratings.r5a = request.POST["r5a"]
            ratings.er5a = request.POST["er5a"]
            ratings.r5b = request.POST["r5b"]
            ratings.er5b = request.POST["er5b"]
            ratings.r5c = request.POST["r5c"]
            ratings.er5c = request.POST["er5c"]
            ratings.r6 = request.POST["r6"]
            ratings.er6 = request.POST["er6"]
            ratings.r7 = request.POST["r7"]
            ratings.er7 = request.POST["er7"]
            ratings.r8 = request.POST["r8"]
            ratings.er8 = request.POST["er8"]
            ratings.save()

            results = calc_agency_targets(agency)
            data["gen1"] = get_comment("1DP")
            data["gen2a"] = get_comment("2DPa")
            data["gen2b"] = get_comment("2DPb")
            data["gen2c"] = get_comment("2DPc")
            data["gen3"] = get_comment("3DP")
            data["gen4"] = get_comment("4DP")
            data["gen5a"] = get_comment("5DPa")
            data["gen5b"] = get_comment("5DPb")
            data["gen5c"] = get_comment("5DPc")
            data["gen6"] = get_comment("6DP")
            data["gen7"] = get_comment("7DP")
            data["gen8"] = get_comment("8DP")

            return HttpResponse(simplejson.dumps(data))
    except:
        import traceback
        traceback.print_exc()
    
def gov_ratings(request, country_id):

    try:
        country = get_object_or_404(Country, id=country_id)
        ratings, _ = GovScorecardRatings.objects.get_or_create(country=country)
        get_comment = lambda indicator : results[indicator]["commentary"]
        data = {}

        if request.method == "GET":
            results = calc_country_targets(country)
            country_data = results


            data["rating1"] = ratings.r1
            data["rating2a"] = ratings.r2a
            data["rating2b"] = ratings.r2b
            data["rating3"] = ratings.r3
            data["rating4"] = ratings.r4
            data["rating5a"] = ratings.r5a
            data["rating5b"] = ratings.r5b
            data["rating6"] = ratings.r6
            data["rating7"] = ratings.r7
            data["rating8"] = ratings.r8

            data["progress1"] = ratings.er1
            data["progress2a"] = ratings.er2a
            data["progress2b"] = ratings.er2b
            data["progress3"] = ratings.er3
            data["progress4"] = ratings.er4
            data["progress5a"] = ratings.er5a
            data["progress5b"] = ratings.er5b
            data["progress6"] = ratings.er6
            data["progress7"] = ratings.er7
            data["progress8"] = ratings.er8

            data["gen1"] = get_comment("1G")
            data["gen2a"] = get_comment("2Ga")
            data["gen2b"] = get_comment("2Gb")
            data["gen3"] = get_comment("3G")
            data["gen4"] = get_comment("4G")
            data["gen5a"] = get_comment("5Ga")
            data["gen5b"] = get_comment("5Gb")
            data["gen6"] = get_comment("6G")
            data["gen7"] = get_comment("7G")
            data["gen8"] = get_comment("8G")

            return HttpResponse(simplejson.dumps(data))
        elif request.method == "POST":
            ratings.r1 = request.POST["r1"]
            ratings.er1 = request.POST["er1"]
            ratings.r2a = request.POST["r2a"]
            ratings.er2a = request.POST["er2a"]
            ratings.r2b = request.POST["r2b"]
            ratings.er2b = request.POST["er2b"]
            ratings.r3 = request.POST["r3"]
            ratings.er3 = request.POST["er3"]
            ratings.r4 = request.POST["r4"]
            ratings.er4 = request.POST["er4"]
            ratings.r5a = request.POST["r5a"]
            ratings.er5a = request.POST["er5a"]
            ratings.r5b = request.POST["r5b"]
            ratings.er5b = request.POST["er5b"]
            ratings.r6 = request.POST["r6"]
            ratings.er6 = request.POST["er6"]
            ratings.r7 = request.POST["r7"]
            ratings.er7 = request.POST["er7"]
            ratings.r8 = request.POST["r8"]
            ratings.er8 = request.POST["er8"]
            ratings.save()

            results = calc_country_targets(country)
            data["gen1"] = get_comment("1G")
            data["gen2a"] = get_comment("2Ga")
            data["gen2b"] = get_comment("2Gb")
            data["gen3"] = get_comment("3G")
            data["gen4"] = get_comment("4G")
            data["gen5a"] = get_comment("5Ga")
            data["gen5b"] = get_comment("5Gb")
            data["gen6"] = get_comment("6G")
            data["gen7"] = get_comment("7G")
            data["gen8"] = get_comment("8G")

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
            results = calc_country_targets(country)
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
    
