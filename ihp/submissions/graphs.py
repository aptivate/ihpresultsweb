from django.views.generic.simple import direct_to_template
from submissions.models import Agency, Country
from indicators import calc_agency_country_indicators, NA_STR

def safe_diff(a, b):
    if a in [None, NA_STR] or b in [None, NA_STR]:
        return None
    else:
        return a - b

def safe_div(a, b):
    if a in [None, NA_STR] or b in [None, NA_STR]:
        return None
    if b == 0:
        return None
    return a / b

def safe_mul(a, b):
    if a in [None, NA_STR] or b in [None, NA_STR]:
        return None
    else:
        return a * b

def format_fig(x):
    if x == None:
        return "0.0"
    return "%.1f" % x

def agencygraphs(request, agency_name, template_name="submissions/agencygraphs.html", extra_context=None, titles=None, yaxes=None, xaxis=None):
    extra_context = extra_context or {}

    agency = Agency.objects.get(agency__iexact=agency_name)
    for indicator in titles:
        titles[indicator] = titles[indicator] % locals()
    for indicator in yaxes:
        yaxes[indicator] = yaxes[indicator] % locals()
    
    data = {}
    abs_values = {}
    for country in agency.countries:
        country_data = {}
        country_abs_values = {}
        indicators = calc_agency_country_indicators(agency, country)
        for indicator in ["2DPa", "2DPb", "2DPc", "3DP", "4DP", "5DPa", "5DPb", "5DPc"]:
            base_val, _, latest_val, _ = indicators[indicator][0]
            country_abs_values[indicator] = (base_val, latest_val) 
            country_data[indicator] = safe_mul(safe_div(safe_diff(latest_val, base_val), base_val), 100)
        data[country.country] = country_data
        abs_values[country.country] = country_abs_values

    extra_context["countries"] = agency.countries    
    extra_context["agency"] = agency.agency    
    extra_context["data"] = sorted(data.items())
    extra_context["abs_values"] = sorted(abs_values.items())
    extra_context["titles"] = titles
    extra_context["yaxes"] = yaxes
    extra_context["xaxis"] = xaxis
    
    return direct_to_template(request, template=template_name, extra_context=extra_context)
    
def countrygraphs(request, country_name, template_name="submissions/countrygraphs.html", extra_context=None, titles=[], yaxes=[], xaxis=""):
    extra_context = extra_context or {}

    country = Country.objects.get(country__iexact=country_name)
    for indicator in titles:
        titles[indicator] = titles[indicator] % locals()
    for indicator in yaxes:
        yaxes[indicator] = yaxes[indicator] % locals()
    
    data = {}
    abs_values = {}
    for agency in country.agencies:
        agency_data = {}
        agency_abs_values = {}
        indicators = calc_agency_country_indicators(agency, country)
        for indicator in ["2DPa", "2DPb", "2DPc", "3DP", "4DP", "5DPa", "5DPb", "5DPc"]:
            base_val, _, latest_val, _ = indicators[indicator][0]
            agency_abs_values[indicator] = (base_val, latest_val) 
            agency_data[indicator] = safe_mul(safe_div(safe_diff(latest_val, base_val), base_val), 100)
        data[agency.agency] = agency_data
        abs_values[agency.agency] = agency_abs_values

    extra_context["agencies"] = country.agencies    
    extra_context["country"] = country.country    
    extra_context["data"] = sorted(data.items())
    extra_context["abs_values"] = sorted(abs_values.items())
    extra_context["titles"] = titles
    extra_context["yaxes"] = yaxes
    extra_context["xaxis"] = xaxis
    
    return direct_to_template(request, template=template_name, extra_context=extra_context)
    
