from django.views.generic.simple import direct_to_template
from functools import partial
from submissions.models import Agency, Country
from indicators import calc_agency_country_indicators, NA_STR, calc_overall_agency_indicators, positive_funcs, calc_country_indicators
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
    "4DP"  : 90,
    "5DPa" : 80, 
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
        "4DP"  : "% of actual health spending planned for that year (4DP) ",
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
        
        graph.subtitle = {
            "text": '* Questions with baseline values from 2008 are not included',
            "align": 'left',
            "x": 50,
            "y": 388,
            "floating" : "true",
        }

        if indicator not in ["5DPc"]:
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

class CountryBarGraph(Chart):
    def __init__(self, countries, chart_name, title, baseline_data, latest_data):
        country_names = map(lambda x: x.country, countries)

        super(CountryBarGraph, self).__init__(chart_name)
        self.chart = {
            "marginTop" : 50,
            "defaultSeriesType": "column",
        }
        self.title = {"text" : title}
        country_names = [country.country for country in countries]
        self.xAxis = {
            "categories" : country_names,
            "labels" : {
                "rotation" : 90,
                "y" : 40,
            }
        } 
        self.yAxis = {"title" : {"text" : "%"}} 
        self.series = [{
            "name" : "Baseline",
            "data" : baseline_data
        }, {
            "name" : "2009",
            "data" : latest_data 
        }]

class TargetCountryBarGraph(CountryBarGraph):
    def __init__(self, countries, chart_name, title, baseline_data, latest_data, target_name, target):
        super(TargetCountryBarGraph, self).__init__(countries, chart_name, title, baseline_data, latest_data)
        self.series.append({
            "name" : target_name,
            "data" : [target] * len(latest_data),
            "type" : "line",
            "color" : "#ff0000",
            "marker" : {
                "enabled" : "false"
            },
        })

    
def additional_graphs(request, template_name="submissions/additionalgraphs.html", extra_context=None):
    extra_context = extra_context or {}
    country_data = get_countries_scorecard_data()
    agency_data = get_agencies_scorecard_data(Agency.objects.get_by_type("Agency"))

    countries = sorted(country_data.keys(), key=lambda x : x.country)

    extra_context["graph_hw"] = CountryBarGraph(
        countries,
        "graph_hw",
        "% of health sector budget spent on health workforce",
        [country_data[country]["indicators"]["other"]["health_workforce_perc_of_budget_baseline"] * 100 for country in countries],
        [country_data[country]["indicators"]["other"]["health_workforce_perc_of_budget_latest"] * 100 for country in countries],
    )

    extra_context["graph_outpatient_visits"] = CountryBarGraph(
        countries,
        "graph_outpatient_visits",
        "Number of outpatient visits per 10,000 population",
        [country_data[country]["indicators"]["other"]["outpatient_visits_baseline"] for country in countries],
        [country_data[country]["indicators"]["other"]["outpatient_visits_latest"] for country in countries],
    )

    extra_context["graph_skilled_medical"] = TargetCountryBarGraph(
        countries,
        "graph_skilled_medical",
        "Skilled medical personnel per 10,000 population",
        [country_data[country]["indicators"]["other"]["skilled_personnel_baseline"] for country in countries],
        [country_data[country]["indicators"]["other"]["skilled_personnel_latest"] for country in countries],
        "WHO Recommended", 23,
    )

    extra_context["graph_health_budget"] = TargetCountryBarGraph(
        countries,
        "graph_health_budget",
        "% of national budget is allocated to health (IHP+ Results data)",
        [country_data[country]["indicators"]["3G"]["baseline_value"] for country in countries],
        [country_data[country]["indicators"]["3G"]["latest_value"] for country in countries],
        "Target", 15,
    )
            
    sort = partial(sorted, key=lambda x : x[1][1])

    def indicator_data(indicator, reverse=False):
        f = lambda x: x
        if reverse: f = lambda x : 100.0 - x
        data = [
            (agency, f(datum[indicator]["cur_val"]))
            for (agency, datum) in agency_data.items()
            if datum[indicator]["cur_val"] not in (NA_STR, None)
        ]
        data = sorted(data, key=lambda x : x[1])
        return data

    class StackedAgencyBarGraph(Chart):
        def __init__(self, chart_name, title, dataset, target_name, target):
            super(StackedAgencyBarGraph, self).__init__(chart_name)
            categories = map(lambda x: x[0].agency, dataset["data"])
            data = map(lambda x: x[1], dataset["data"])

            data1 = data
            data2 = map(lambda x: 100 - x, data)

            self.chart = {
                "marginTop" : 50,
                "defaultSeriesType": "column",
            }
            self.title = {"text" : title}
            self.xAxis = {
                "categories" : categories,
                "labels" : {
                    "rotation" : 90,
                    "y" : 40,
                }
            } 
            self.yAxis = {
                "title" : {"text" : "%"},
                "max" : 100
            } 
            self.series = [{
                "name" : dataset["name2"],
                "data" : data2, 
                "color" : "#AA4643"
            }, {
                "name" : dataset["name1"],
                "data" : data1,
                "color" : "#4572A7"
            }, {
                "name" : target_name,
                "data" : [target] * len(categories),
                "type" : "line",
                "color" : "#ff0000",
                "marker" : {
                    "enabled" : "false"
                },
            }]

            self.plotOptions = {"column" : {"stacking" : "percent"}}

    extra_context["graph_pfm"] = StackedAgencyBarGraph(
        "graph_pfm",
        "% of aid using national PFM systems",
        {
            "name1" : "Total health aid using PFM systems (Q15)",
            "name2" : "Total health aid not using PFM systems (Q14 - Q15)",
            "data" : indicator_data("5DPb", reverse=True)
        },
        "target", 80
    )
        
    extra_context["graph_procurement"] = StackedAgencyBarGraph(
        "graph_procurement",
        "% of aid using national procurement systems",
        {
            "name1" : "Total health aid using procurement systems (Q13)",
            "name2" : "Total health aid not using procurement systems (Q12 - Q13)",
            "data" : indicator_data("5DPa", reverse=True)
        },
        "target", 80
    )

    extra_context["graph_multi_year"] = StackedAgencyBarGraph(
        "graph_multi_year",
        "% of aid provided through multi-year commitments",
        {
            "name1" : "% of multi-year commitments",
            "name2" : "% not provided through multi-year commitments",
            "data" : indicator_data("3DP")
        },
        "target", 90
    )

    extra_context["graph_pba"] = StackedAgencyBarGraph(
        "graph_pba",
        "% of aid using Programme Based Approaches (PBAs)",
        {
            "name1" : "% of health sector aid using PBAs",
            "name2" : "% of health sector aid not using PBAs",
            "data" : indicator_data("2DPc")
        },
        "target", 66
    )

    extra_context["graph_tc"] = StackedAgencyBarGraph(
        "graph_tc",
        "% of capacity development provided through coordinated programmes",
        {
            "name1" : "TC through coordinated programmes (Q5)",
            "name2" : "TC not through coordinated programmes (Q4 - Q5)",
            "data" : indicator_data("2DPb")
        },
        "target", 50
    )

    extra_context["graph_aob"] = StackedAgencyBarGraph(
        "graph_aob",
        "% of aid reported on budget",
        {
            "name2" : "Total health aid not on budget",
            "name1" : "Total health aid reported on budget",
            "data" : indicator_data("2DPa", reverse=True)
        },
        "target", 85
    )

    return direct_to_template(request, template=template_name, extra_context=extra_context)

def government_graphs(request, template_name="submission/country_graphs_by_indicator.html", extra_context=None):
    extra_context = extra_context or {}
    countries = sorted(Country.objects.all(), key=lambda x: x.country)
    data_3G = dict([(c, calc_country_indicators(c)["3G"]) for c in countries])
    data_4G = dict([(c, calc_country_indicators(c)["4G"]) for c in countries])

    extra_context["graph_3G"] = TargetCountryBarGraph(
        countries,
        "graph_3G",
        "% of national budget is allocated to health (IHP+ Results data)",
        [data_3G[country][0][0] for country in countries],
        [data_3G[country][0][2] for country in countries],
        "Target", 15,
    )

    extra_context["graph_4G"] = CountryBarGraph(
        countries,
        "graph_4G",
        "% of health sector funding disbursed against the approved annual budget",
        [data_4G[country][0][0] for country in countries],
        [data_4G[country][0][2] for country in countries],
    )
    
    return direct_to_template(request, template=template_name, extra_context=extra_context)
