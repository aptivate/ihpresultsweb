import re
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from submissions.models import Agency, DPScorecardSummary, DPScorecardRatings, GovScorecardRatings, GovScorecardComments, Country, CountryScorecardOverrideComments, GovQuestion, DPQuestion, Language
import models
from target import calc_agency_ratings, calc_country_ratings
import indicators
import target
import country_scorecard

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
                
                setattr(ratings, "r%s" % core_indicator, request.POST["r%s" % core_indicator])
                setattr(ratings, "er%s" % core_indicator, request.POST["er%s" % core_indicator])
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
        country = get_object_or_404(models.Country, id=country_id)
        ratings, _ = models.GovScorecardRatings.objects.get_or_create(country=country)

        comments_en, _ = GovScorecardComments.objects.get_or_create(
            country=country, 
            language=Language.objects.filter(language="English")
        )
        comments_fr, _ = GovScorecardComments.objects.get_or_create(
            country=country, 
            language=Language.objects.filter(language="French")
        )

        get_comment = lambda indicator : results[indicator]["commentary"]
        data = {}
        indicators = ["1", "2a", "2b", "3", "4", "5a", "5b", "6", "7", "8"]
        other_indicators = ["hmis1", "jar1", "hsp1", "hsp2", "hsm1", "hsm4"]

        if request.method == "GET":
            results = calc_country_ratings(country)
            country_data = results

            for indicator in indicators:
                data["r%s" % indicator] = getattr(ratings, "r%s" % indicator)
                data["er%s_en" % indicator] = getattr(comments_en, "er%s" % indicator)
                data["er%s_fr" % indicator] = getattr(comments_fr, "er%s" % indicator)
                data["gr%s" % indicator] = get_comment(indconv(indicator))

            for indicator in other_indicators:
                data[indicator] = getattr(ratings, indicator)

            return HttpResponse(simplejson.dumps(data))
        elif request.method == "POST":
            for indicator in indicators:
                setattr(ratings, "r%s" % indicator, request.POST["r%s" % indicator]) 
                setattr(comments_en, "er%s" % indicator, request.POST["er%s_en" % indicator]) 
                setattr(comments_fr, "er%s" % indicator, request.POST["er%s_fr" % indicator]) 

            for indicator in other_indicators:
                setattr(ratings, indicator, request.POST[indicator])

            ratings.save()
            comments_en.save()
            comments_fr.save()

            results = calc_country_ratings(country)

            for indicator in indicators:
                data["gen%s" % indicator] = get_comment(indconv(indicator))

            return HttpResponse(simplejson.dumps(data))
    except:
        import traceback
        traceback.print_exc()
    
def country_scorecard_overrides(request, country_id):

    class LazyCommentsLoader(object):
        def __init__(self, country):
            self._map = {}
            self._country = country
        def __getitem__(self, language):
            try:
                if type(language) != Language:
                    language = Language.objects.get(language=language)
                if not language in self._map:
                    comments = CountryScorecardOverrideComments.objects.get(country=self._country, language=language)
                    self._map[language] = comments
                return self._map[language]
            except Language.DoesNotExist:
                return None
            except CountryScorecardOverrideComments.DoesNotExist:
                return None

    override_fields = ["RF2", "RF3", "DBR2", "HMIS2", "JAR4", "PFM2", "PR2", "PF2", "CD2", "TA2"]
    try:
        country = get_object_or_404(Country, id=country_id)
        data = {}

        if request.method == "GET":
            data = {}

            for language in models.Language.objects.all():
                tmp_data = country_scorecard.get_country_export_data(country, language)
                for field in override_fields:
                    data["%s_%s" % (field.lower(), language.language)] = tmp_data[field]

            return HttpResponse(simplejson.dumps(data))
        elif request.method == "POST":
            ratings, _ = models.GovScorecardRatings.objects.get_or_create(country=country)
            comments_loader = LazyCommentsLoader(country)
            for key in request.POST.keys():
                if key in ratings.__dict__:
                    ratings.__dict__[key] = request.POST[key]
                elif len(key.split("_")) == 2:
                    field, language = key.split("_")
                    comments = comments_loader[language]
                    if comments and hasattr(comments, field):
                        setattr(comments, field, request.POST[key])

            ratings.save()
            for comments in comments_loader._map.values():
                comments.save()

            return HttpResponse(simplejson.dumps(data))
    except:
        import traceback
        traceback.print_exc()
    
