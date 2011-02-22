from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import submissions.target
import submissions.views
from submissions.models import Submission

class Category:
    code = property()
    expected_result = property()
    indicators = property()

class Indicator:
    code = property()
    rating = property()
    overall_progress = property()

def _group_and_sort_indicators(ratings, titles):
    categories = {}
    
    for indicator_code in sorted(ratings.keys()):
        i = Indicator()
        i.code = indicator_code
        
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

            if category_code in titles:
                category.expected_result = titles[category_code]
            else:
                category.expected_result = (category_code + " Lorem " +
                    "ipsum dolor sit amet, consectetur adipiscing elit. " +
                    "Donec condimentum velit id sapien iaculis rhoncus.")
        
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
    p, np = submissions.target.get_country_progress(agency)
    
    context = dict(agency=agency,
        categories=_group_and_sort_indicators(ratings, 
            agency_indicator_descriptions),
        progress_countries=p.values(),
        no_progress_countries=np.values())
    
    return render_to_response('agency_scorecard.html',
        RequestContext(request, context))

def country_scorecard_page(request, country_name):
    country = submissions.models.Country.objects.get(country=country_name)
    ratings = submissions.target.calc_country_ratings(country)
    p, np = submissions.target.get_agency_progress(country)
    
    titles = {}
    
    context = dict(country=country,
        categories=_group_and_sort_indicators(ratings,
            country_indicator_descriptions),
        progress_agencies=p.values(),
        no_progress_agencies=np.values(),
        raw_data=submissions.views.get_countries_export_data()[country])
    
    return render_to_response('country_scorecard.html',
        RequestContext(request, context))
