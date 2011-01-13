from django.views.generic.simple import direct_to_template
from functools import partial
from submissions.models import Agency, Country
from indicators import calc_agency_country_indicators, NA_STR, calc_overall_agency_indicators, positive_funcs
from views import get_countries_scorecard_data, get_agencies_scorecard_data
from highcharts import Chart

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

# TODO - this shouldn't be hardcoded like this - should rather from the db but 
# but these values seem to be different to the ones that i have
target_values = {
    "2DPa" : 85,
    "2DPb" : 50,
    "2DPc" : 66,
    "3DP"  : 90,
    "5DPa" : 66, 
    "5DPb" : 80, 
    "5DPc" : 0, 
}

def projectiongraphs(request, template_name="submissions/projectiongraphs.html", extra_context=None):
    extra_context = extra_context or {}
    titles = {
        "2DPa" : "Projected time required to meet On Budget target <br>(based on current levels of performance):2007 Baseline",
        "5DPb" : "Projected time required to meet PFM target <br>(based on current levels of performance):2007 Baseline",
    }
    indicators = calc_overall_agency_indicators(funcs=positive_funcs)

    for indicator in titles.keys():
        (baseline_value, baseline_year, latest_value, latest_year) = indicators[indicator][0]
        baseline_year, latest_year = int(baseline_year), int(latest_year)
        target_value = target_values[indicator]

        # Find the intersection point between the horizontal target line and the trend line
        # i.e. x = (y - c)/m 
        m = (latest_value - baseline_value) / (latest_year - baseline_year)
        c = baseline_value
        intersection = (target_value - c) / m  + baseline_year
        y = lambda x : m * (x - baseline_year) + c

        start_year = baseline_year
        end_year = int(round(intersection, 0) + 1)
        target_data = [target_value] * (end_year - start_year + 1)
        actual_data = [y(year) for year in range(start_year, latest_year + 1)]
        projected_data = [(year - start_year, y(year)) for year in range(latest_year, end_year + 1)]

        graph = Chart("graph_%s" % indicator.lower())
        graph.chart = {
            "marginTop" : 50,
            "defaultSeriesType": "line",
        }

        graph.title = {"text" : titles[indicator]}
        graph.xAxis = {"categories" : range(start_year, end_year + 1)} 
        graph.yAxis = {"title" : {"text" : ""}} 

        graph.series = [{
            "name" : "Actual",
            "data" : actual_data
        }, {
            "name" : "Projected",
            "data" : projected_data,
            "dashStyle" : "shortDash",
            "color" : "#89A54E",
        }, {
            "name": "Target",
            "data": target_data,
            "marker": {
               "enabled": "false"
            },
        }]

        extra_context["graph_%s" % indicator] = graph 

    return direct_to_template(request, template=template_name, extra_context=extra_context)


def highlevelgraphs(request, template_name="submissions/highlevelgraphs.html", extra_context=None, titles=None):
    extra_context = extra_context or {}

    titles = titles or {
        "2DPa" : "% of total funding on-budget (2DPa)",
        "2DPb" : "% of TC implemented through coordinated programmes (2DPb)",
        "2DPc" : "% of funding using Programme Based Approaches (2DPc) ",
        "3DP"  : "% of aid provided through multi-year commitments (3DP) ",
        "5DPa" : "% of funding for procurement using national procurement systems (5DPa)", 
        "5DPb" : "% of funding using national PFM systems (5DPb)", 
        "5DPc" : "Number of Parallel Project Implementation Units", 
    }

    indicators = calc_overall_agency_indicators(funcs=positive_funcs)
    for indicator in indicators:
        (baseline_value, _, latest_value, _) = indicators[indicator][0]

        graph = Chart("graph_%s" % indicator.lower())

        graph.title = {"text" : titles[indicator]}
        graph.xAxis = {"categories" : ["Baseline", "2009"]} 

        graph.series = [{
            "name" : "Aggregated Data",
            "type" : "column",
            "data" : [float(baseline_value), float(latest_value)]
        }]

        if indicator != "5DPc":
            graph.series.append({
                "type" : "line",
                "name" : "Target",
                "data" : [target_values[indicator]] * 2,
                "dashStyle" : "shortDash",
                "marker" : {
                    "enabled" : "false"
            },
        })

        extra_context["graph_%s" % indicator] = graph 


    return direct_to_template(request, template=template_name, extra_context=extra_context)

def agencygraphs(request, agency_name, template_name="submissions/agencygraphs.html", extra_context=None, titles=None, yaxes=None, xaxis=None):
    extra_context = extra_context or {}

    titles = dict(titles)
    yaxes = dict(yaxes)
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

    titles = dict(titles)
    yaxes = dict(yaxes)
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
    
def additional_graphs(request, template_name="submissions/additionalgraphs.html", extra_context=None):
    extra_context = extra_context or {}
    country_data = get_countries_scorecard_data()
    agency_data = get_agencies_scorecard_data()

    extra_context["hw_spend"] = {
        "title" : "% of health sector budget spent on health workforce",
        "data" : dict(
            (
                country, 
                {
                    "baseline" : datum["indicators"]["other"]["health_workforce_perc_of_budget_baseline"] * 100,
                    "latest" : datum["indicators"]["other"]["health_workforce_perc_of_budget_latest"] * 100, 
                }
            ) 
            for country, datum in country_data.items()
        )
    }

    extra_context["outpatient_visits"] = {
        "title" : "Number of outpatient visits per 10,000 population",
        "y-axis" : "",
        "data" : dict(
            (
                country, 
                {
                    "baseline" : datum["indicators"]["other"]["outpatient_visits_latest"],
                    "latest" : datum["indicators"]["other"]["outpatient_visits_latest"], 
                }
            ) 
            for country, datum in country_data.items()
        )
    }

    extra_context["skilled_medical"] = {
        "title" : "Skilled medical personnel per 10,000 population",
        "y-axis" : "",
        "target" : {
            "name" : "WHO Recommended",
            "value" : 23,
        },
        "data" : dict(
            (
                country, 
                {
                    "baseline" : datum["indicators"]["other"]["skilled_personnel_baseline"],
                    "latest" : datum["indicators"]["other"]["skilled_personnel_latest"], 
                }
            ) 
            for country, datum in country_data.items()
        )
    }

    extra_context["health_budget"] = {
        "title" : "% of national budget is allocated to health (IHP+ Results data)",
        "target" : {
            "value" : 15,
        },
        "y-axis" : "% allocated to health",
        "data" : dict(
            (
                country, 
                {
                    "baseline" : datum["indicators"]["3G"]["baseline_value"],
                    "latest" : datum["indicators"]["3G"]["latest_value"],
                }
            ) 
            for country, datum in country_data.items()
        )
    }
    
    sort = partial(sorted, key=lambda x : x[1][1])

    def indicator_data(indicator):
        data = [
            (
                agency, [
                    datum[indicator]["cur_val"], 
                    100 - datum[indicator]["cur_val"],
                ]
            )
            for (agency, datum) in agency_data.items()
            if datum[indicator]["cur_val"] not in (NA_STR, None)
        ]
        return sort(data)

    extra_context["pfm"] = {
        "title" : "% of aid using national PFM systems",
        "target" : {
            "value" : 80,
        },
        "series" : [
            "Total health aid not using PFM systems (Q14 - Q15)",
            "Total health aid using PFM systems (Q15)",
        ],
        "data" : indicator_data("5DPb"),
    }

    extra_context["procurement"] = {
        "title" : "% of aid using national procurement systems",
        "target" : {
            "value" : 80,
        },
        "series" : [
            "Total health aid not using procurement systems (Q12 - Q13)",
            "Total health aid using procurement systems (Q13)",
        ],
        "data" : indicator_data("5DPa"),
    }

    extra_context["multi_year"] = {
        "title" : "% of aid provided through multi-year commitments",
        "target" : {
            "value" : 90,
        },
        "series" : [
            "% not provided through multi-year commitments",
            "% of multi-year commitments",
        ],
        "data" : indicator_data("3DP"),
    }

    extra_context["pba"] = {
        "title" : "% of aid using Programme Based Approaches (PBAs)",
        "target" : {
            "value" : 66,
        },
        "series" : [
            "% of health sector aid not using PBAs",
            "% of health sector aid using PBAs",
        ],
        "data" : indicator_data("2DPc"),
    }

    extra_context["tc"] = {
        "title" : "% of capacity development provided through coordinated programmes",
        "target" : {
            "value" : 50,
        },
        "series" : [
            "TC not through coordinated programmes (Q4 - Q5)",
            "TC through coordinated programmes (Q5)",
        ],
        "data" : indicator_data("2DPb"),
    }

    extra_context["aid_on_budget"] = {
        "title" : "% of aid reported on budget",
        "target" : {
            "value" : 85,
        },
        "series" : [
            "Total health aid not on budget",
            "Total health aid reported on budget",
        ],
        "data" : indicator_data("2DPa"),
    }

    return direct_to_template(request, template=template_name, extra_context=extra_context)

