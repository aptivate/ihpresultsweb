from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import submissions.country_scorecard
import submissions.target
import submissions.views
import submissions.table_views
from submissions.models import Submission, Language, AgencyProfile
import logging

class Category:
    code = property()
    expected_result = property()
    indicators = property()
    agency_report = property()

class Indicator:
    code = property()
    rating = property()
    overall_progress = property()

def _group_and_sort_indicators(ratings, titles):
    categories = {}
    
    for indicator_code in sorted(ratings.keys()):
        i = Indicator()
        i.code = indicator_code
        
        first_letter = indicator_code[0]
        if first_letter == 'Q':
            continue
        
        last_letter = indicator_code[-1]
        if last_letter.islower():
            category_code = indicator_code[0:-1]
        else:
            category_code = indicator_code
            
        if not category_code in categories:
            category = Category()
            categories[category_code] = category
            category.code = category_code
            category.indicators = []
            category.expected_result = titles[category_code]
        
        rating = ratings[indicator_code]
        i.rating = rating['target']
        i.overall_progress = rating['commentary']

        category = categories[category_code] 
        category.indicators.append(i)
        
        # print "%s indicators = %s" % (category_code, category.indicators)

    category_list = []
    for category_code in sorted(categories.keys()):
        category_list.append(categories[category_code])
        
    return category_list

agency_indicator_descriptions = {
    '1DP': "Commitments are documented and mutually agreed.",
    '2DP': ("Support is based on country plans & strategies, " + 
        "including to strengthen Health Systems."),
    '3DP': "Funding commitments are long-term.",
    '4DP': "Funds are disbursed predictably, as committed.",
    '5DP': ("Country systems for procurement & public financial management " +
        "are used & strengthened."),
    '6DP': "Resources are being managed for Development Results.",
    '7DP': "Mutual accountability is being demonstrated.",
    '8DP': "Civil Society actively engaged.",
    }

country_indicator_descriptions = {
    '1G': 'Commitments are documented and mutually agreed.',
    '2G': ('Support is based on country plans & strategies, including ' +
        'to strengthen Health Systems.'),
    '3G': 'Funding commitments are long-term.',
    '4G': 'Funds are disbursed predictably, as committed.',
    '5G': ('Country systems for procurement & public financial management ' +
        'are used & strengthened.'),
    '6G': 'Resources are being managed for Development Results.',
    '7G': 'Mutual accountability is being demonstrated.',
    '8G': 'Civil Society actively engaged.',
    }

def agency_scorecard_page(request, agency_name):
    agency = submissions.models.Agency.objects.get(agency=agency_name)
    ratings = submissions.target.calc_agency_ratings(agency)
    np, p = submissions.target.get_country_progress(agency)
    english = Language.objects.get(language="English")
    categories = _group_and_sort_indicators(ratings, 
        agency_indicator_descriptions)
    agency_report = submissions.models.DPScorecardSummary.objects.get(
        agency=agency, language=english)
    
    for category in categories:
        field_name = "erb%s" % category.code[0]
        category.agency_report = getattr(agency_report, field_name)
    
    context = dict(agency=agency,
        categories=categories,
        progress_countries=p.values(),
        no_progress_countries=np.values(),
        profile=submissions.models.AgencyProfile.objects.get(agency=agency,
            language=english))
    
    return render_to_response('agency_scorecard.html',
        RequestContext(request, context))

def _format_and_sort_ratings(ratings):
    values = []

    for indicator_code, rating_data in ratings.iteritems():
        rating_data['baseline_value_fmt'] = (
            submissions.table_views.tbl_float_format(rating_data['base_val']))
        rating_data['latest_value_fmt'] = (
            submissions.table_views.tbl_float_format(rating_data['cur_val']))
        values.append((indicator_code, rating_data))
        
    values = sorted(values, key=lambda x: x[0])
    return values

def country_scorecard_page(request, country_name):
    country = submissions.models.Country.objects.get(country=country_name)
    ratings = submissions.target.calc_country_ratings(country)
    np, p = submissions.target.get_agency_progress(country)
    
    context = dict(country=country,
        categories=_group_and_sort_indicators(ratings,
            country_indicator_descriptions),
        progress_agencies=p.values(),
        no_progress_agencies=np.values(),
        raw_data=submissions.country_scorecard.get_country_export_data(country),
        values=_format_and_sort_ratings(ratings),
        country_spms_numeric=country_spms_numeric)
    
    return render_to_response('country_scorecard.html',
        RequestContext(request, context))

def agency_spm_countries_table(request, agency_name, indicator_name):
    agency = submissions.models.Agency.objects.get(agency=agency_name)
    countries = submissions.models.Country.objects.all().order_by("country")
    values = []
    
    for country in countries:
        if country in agency.countries:
            indicators = submissions.views.calc_agency_country_indicators(agency,
                country, submissions.indicators.positive_funcs)
            ratings = submissions.views.country_agency_indicator_ratings(country, agency)

            base_val, base_year, latest_val, _ = indicators[indicator_name][0]
            country_abs_values = {
                "baseline_value" : submissions.table_views.tbl_float_format(base_val), 
                "latest_value" : submissions.table_views.tbl_float_format(latest_val), 
                "rating" : ratings[indicator_name],
                "cellclass" : "",
            } 
            values.append((country, country_abs_values))
        else:
            # skip rows for countries where this agency does not work. refs #1013
            pass
            
    values = sorted(values, key=lambda x: x[0].country)

    return render_to_response('agency_spm_countries_table.html',
        RequestContext(request, dict(agency=agency,
            indicator_name=indicator_name, values=values)))

country_spms_numeric = ("3G", "4G", "5Ga", "5Gb", "8G")

def country_spms_table(request, country_name):
    country = submissions.models.Country.objects.get(country=country_name)
    ratings = submissions.target.calc_country_ratings(country)

    return render_to_response('country_spms_table.html',
        RequestContext(request, dict(country=country,
            values=_format_and_sort_ratings(ratings),
            country_spms_numeric=country_spms_numeric)))

def agency_country_spms_table(request, agency_name, country_name):
    agency = submissions.models.Agency.objects.get(agency=agency_name)
    country = submissions.models.Country.objects.get(country=country_name)
    values = []

    indicators = submissions.views.calc_agency_country_indicators(agency,
        country, submissions.indicators.positive_funcs)
    ratings = submissions.views.country_agency_indicator_ratings(country, agency)

    for indicator_name, raw_values in indicators.iteritems():
        base_val, base_year, latest_val, _ = raw_values[0]
        indicator_abs_values = {
            "baseline_value" : submissions.table_views.tbl_float_format(base_val), 
            "latest_value" : submissions.table_views.tbl_float_format(latest_val), 
            "rating" : ratings[indicator_name],
            "cellclass" : "",
        } 
        values.append((indicator_name, indicator_abs_values))

    values = sorted(values, key=lambda x: x[0])

    return render_to_response('agency_country_spms_table.html',
        RequestContext(request, dict(agency=agency,
            country=country, values=values)))

def unicode_test(request):
    return HttpResponse(submissions.models.GovScorecardComments.objects.get(id=9).er1)