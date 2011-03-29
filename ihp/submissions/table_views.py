from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404

import models
import target
import indicators
from indicators import NA_STR
import consts
import translations

def tbl_float_format(x, places=0):
    if type(x) == float:
        if places == 0:
            return int(round(x, places))
        else:
            return round(x, places) 
    elif x == NA_STR:
        return "N/A"
    elif x == None:
        return None
    return x

def perc_change(base_val, latest_val):
    none_vals = [None, NA_STR]
    if type(base_val) == str or type(latest_val) == str:
        return None
    if base_val in none_vals or latest_val in none_vals:
        return None
    if base_val == 0:
        return None
    return (latest_val - base_val) / base_val * 100.0

def agency_table_by_indicator(request, indicator, language="English", template_name="submissions/agency_table_by_indicator.html", extra_context=None):
    dp_gov_map = {
        "1DP" : "1G",
        "6DP" : "6G",
        "7DP" : "7G",
        "8DP" : "8G",
    }
    extra_context = extra_context or {} 
    extra_context["translation"] = request.translation

    country_calcs = None
    countries = models.Country.objects.all().order_by("country")
    if indicator in dp_gov_map:
        gov_indicator = dp_gov_map[indicator]
        country_calcs = [(c, target.calc_country_ratings(c)[gov_indicator]) for c in countries]
    
    agencies = []
    for agency in models.Agency.objects.all():
        agency_values = []
        for country in countries:
            if country in agency.countries:
                inds = indicators.calc_agency_country_indicators(agency, country, indicators.positive_funcs)
                ratings = target.country_agency_indicator_ratings(country, agency)

                base_val, base_year, latest_val, cur_year = inds[indicator][0]
                country_abs_values = {
                    "baseline_value" : tbl_float_format(base_val), 
                    "base_year" : base_year,
                    "latest_value" : tbl_float_format(latest_val), 
                    "cur_year" : cur_year,
                    "rating" : ratings[indicator],
                    "cellclass" : "",
                } 
            else:
                country_abs_values = {
                    "baseline_value" : "",
                    "base_year" : "",
                    "latest_value" : "",
                    "cur_year" : "",
                    "rating" : "",
                    "cellclass" : "notactive",
                } 
                
            agency_values.append((country, country_abs_values))
        agency_values = sorted(agency_values, key=lambda x: x[0].country)
        agencies.append((agency, agency_values))

    agencies = sorted(agencies, key=lambda x: x[0].agency)
    extra_context["agencies"] = agencies
    extra_context["countries"] = countries
    extra_context["country_calcs"] = country_calcs
    
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def agency_table_by_agency(request, agency_id, language="English", template_name="submissions/agency_table.html", extra_context=None):
    extra_context = extra_context or {} 
    agency = get_object_or_404(models.Agency, pk=agency_id)

    extra_context["translation"] = translation = request.translation
    abs_values = {}
    for country in agency.countries:
        country_abs_values = {}
        inds = indicators.calc_agency_country_indicators(agency, country, indicators.positive_funcs)
        ratings = target.country_agency_indicator_ratings(country, agency)
        for indicator in inds:
            base_val, base_year, latest_val, latest_year = inds[indicator][0]
            country_abs_values[indicator] = {
                "base_val" : tbl_float_format(base_val), 
                "latest_val" : tbl_float_format(latest_val), 
                "perc_change" : tbl_float_format(perc_change(base_val, latest_val)),
                "base_year" : base_year,
                "latest_year" : latest_year,
                "rating" : ratings[indicator]
            } 
        abs_values[country.country] = country_abs_values
    extra_context["abs_values"] = sorted(abs_values.items())
    extra_context["spm_map"] = translation.spm_map
    extra_context["institution_name"] = translation.by_agency_title % agency.agency
    
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def agency_table_by_country(request, country_id, language="English", template_name="submissions/agency_table.html", extra_context=None):
    extra_context = extra_context or {} 
    country = get_object_or_404(models.Country, pk=country_id)

    extra_context["translation"] = translation = request.translation
    abs_values = {}
    for agency in country.agencies:
        ratings = target.country_agency_indicator_ratings(country, agency)
        agency_abs_values = {}
        inds = indicators.calc_agency_country_indicators(agency, country, indicators.positive_funcs)
        for indicator in inds:
            base_val, base_year, latest_val, latest_year = inds[indicator][0]
            agency_abs_values[indicator] = {
                "base_val" : tbl_float_format(base_val), 
                "latest_val" : tbl_float_format(latest_val), 
                "perc_change" : tbl_float_format(perc_change(base_val, latest_val)), 
                "base_year" : base_year,
                "latest_year" : latest_year,
                "rating" : ratings[indicator]
            } 
        abs_values[agency.agency] = agency_abs_values
    extra_context["abs_values"] = sorted(abs_values.items())
    extra_context["spm_map"] = translation.spm_map
    extra_context["institution_name"] = translation.by_country_title % country.country
    
    return direct_to_template(request, template=template_name, extra_context=extra_context)

def gbs_table(request, agency_id, template_name="submissions/gbs_table.html", extra_context=None):
    extra_context = extra_context or {} 
    gbsagency = models.Agency.objects.all_types().get(pk=agency_id)
    agency = get_object_or_404(models.Agency, agency=gbsagency.agency.replace("GBS", ""))

    extra_context["agency"] = agency
    extra_context["agency_data"] = target.calc_agency_ratings(agency)
    extra_context["gbs_agency_data"] = target.calc_agency_ratings(gbsagency)

    return direct_to_template(request, template=template_name, extra_context=extra_context)

def country_table(request, language="English", template_name="submissions/country_table.html", extra_context=None):
    extra_context = extra_context or {}
    extra_context["translation"] = translation = request.translation
    abs_values = {}
    for country in models.Country.objects.all().order_by("country"):
        country_abs_values = {}
        country_ratings = target.calc_country_ratings(country)
        inds = indicators.calc_country_indicators(country, indicators.positive_funcs)
        for indicator in inds:
            tpl = inds[indicator][0]
            base_val, base_year, latest_val, latest_year = tpl
            rating = country_ratings[indicator]["target"]

            if type(base_val) == str: base_val = base_val.upper()
            if type(latest_val) == str: latest_val = latest_val.upper()
            if indicator == "2Gb":
                # The indicator turns this into 100/0
                # This code turns it back - to much effort
                # to figure out why it does this
                base_val = "Y" if base_val == 100 else "N"
                latest_val = "Y" if latest_val == 100 else "N"
            if indicator == "2Ga":
                base_val1 = base_val[0] if base_val else None
                base_val2 = base_val[1] if base_val else None
                latest_val1 = latest_val[0] if latest_val else None
                latest_val2 = latest_val[1] if latest_val else None

                country_abs_values["2Ga1"] = (
                    tbl_float_format(base_val1), 
                    tbl_float_format(latest_val1), 
                    None,
                    base_year,
                    rating
                ) 
                country_abs_values["2Ga2"] = (
                    tbl_float_format(base_val2), 
                    tbl_float_format(latest_val2), 
                    None,
                    base_year,
                    rating,
                ) 
            else:
                decimal_places = {
                    "5Ga" : 1
                }
                places = decimal_places.get(indicator, 0)
                country_abs_values[indicator] = (
                    tbl_float_format(base_val, places), 
                    tbl_float_format(latest_val, places), 
                    tbl_float_format(perc_change(base_val, latest_val), places),
                    base_year,
                    rating
                ) 
        abs_values[country.country] = country_abs_values
    extra_context["abs_values"] = sorted(abs_values.items())
    extra_context["spm_map"] = translation.gov_spm_map
        
    return direct_to_template(request, template=template_name, extra_context=extra_context)
    

