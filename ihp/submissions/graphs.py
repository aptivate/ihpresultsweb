from django.views.generic.simple import direct_to_template
from functools import partial
from submissions.models import Agency, Country
from indicators import calc_agency_country_indicators, NA_STR, calc_overall_agency_indicators, positive_funcs, calc_country_indicators
from highcharts import Chart, ChartObject
import country_scorecard
import agency_scorecard

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

class IHPChart(Chart):
    def __init__(self, target_element, source):
        super(IHPChart, self).__init__(target_element)
        self._source = source
        self.colors = [
            '#2D5352',
            '#82A8A0',
            '#F68B1F',
            '#C4D82E',
            '#4572A7', 
            '#AA4643', 
            '#89A54E', 
            '#80699B', 
            '#3D96AE', 
            '#DB843D', 
            '#92A8CD', 
            '#A47D7C', 
            '#B5CA92'
        ]

    def __str__(self):
        chart = self.__dict__.setdefault("chart", ChartObject())
        if type(chart) == dict:
            chart["renderTo"] = self._target_element
        else:
            chart.renderTo = self._target_element

        content = super(Chart, self).__str__().strip()
        var_name = self.var_name
        source = self._source
        return """ 
var %(var_name)s; // globally available
$(document).ready(function() {
    %(var_name)s = new Highcharts.Chart(
        %(content)s
    );
    $('tspan').last().text('%(source)s');
});
""" % locals()

class DPChart(IHPChart):
    def __init__(self, target_element):
        super(DPChart, self).__init__(target_element, "Source: DP data returns")

class CountryChart(IHPChart):
    def __init__(self, target_element):
        super(CountryChart, self).__init__(target_element, "Source: Country data returns/CSO data returns")

        

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

        graph = DPChart("graph_%s" % indicator.lower())
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
        "2DPa" : "2DPa: Aggregate proportion of funding on country budget",
        "2DPb" : "2DPb: Aggregate proportion of partner support for capacity-development <br/>provided through coordinated programmes in line with national strategies",
        "2DPc" : "2DPc: Aggregate proportion of partner support <br/>provided as programme based approaches",
        "3DP"  : "3DP: Aggregate proportion partner support <br/>provided through multi-year commitments",
        "4DP"  : "% of actual health spending planned for that year (4DP) ",
        "5DPa" : "5DPa: Aggregate partner use of country procurement systems", 
        "5DPb" : "5DPb: Aggregate partner use of country public financial management systems", 
        "5DPc" : "5DPc: Aggregate number of parallel Project Implementation Units (PIUs)", 
    }

    yaxes = {
        "2DPa" : "%",
        "2DPb" : "%",
        "2DPc" : "%",
        "3DP"  : "%",
        "4DP"  : "%",
        "5DPa" : "%", 
        "5DPb" : "%", 
        "5DPc" : "Total number of PIUs"
    }

    indicators = calc_overall_agency_indicators(funcs=positive_funcs)
    for indicator in indicators:
        (baseline_value, _, latest_value, _) = indicators[indicator][0]

        graph = DPChart("graph_%s" % indicator.lower())

        graph.title = {"text" : titles[indicator]}
        graph.xAxis = {"categories" : ["Baseline", "2009"]} 

        if "<br" in titles[indicator]:
            graph.chart = {
                "marginTop" : 60
            }

        graph.series = [{
            "name" : "Aggregated Data",
            "type" : "column",
            "data" : [float(baseline_value), float(latest_value)]
        }]
        
        graph.subtitle = {
            "text": '* Data with baseline values from 2008 are not included',
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
                "color": "#F68B1F",
            })

        if indicator in yaxes:
            graph.yAxis = {"title" : {"text" : yaxes[indicator]}} 
            pass

        graph.legend = {
            "enabled" : "false"
        }

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

class CountryBarGraph(CountryChart):
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
                "rotation" : -90,
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
            "color" : "#F68B1F",
            "marker" : {
                "enabled" : "false"
            },
        })

    
def additional_graphs(request, template_name="submissions/additionalgraphs.html", extra_context=None):
    extra_context = extra_context or {}
    agency_data = dict([(agency, agency_scorecard.get_agency_scorecard_data(agency)) for agency in Agency.objects.all()])
    country_data = dict([(country, country_scorecard.get_country_export_data(country)) for country in Country.objects.all()])

    countries = sorted(country_data.keys(), key=lambda x : x.country)

    # TODO
    # Request from James to remove overly large values
    remove_large = lambda x : 0 if x > 100 else x

    extra_context["graph_hw"] = CountryBarGraph(
        countries,
        "graph_hw",
        "Proportion of health sector budget spent on Human Resources for Health (HRH)",
        [remove_large(country_data[country]["indicators"]["other"]["health_workforce_perc_of_budget_baseline"] * 100) for country in countries],
        [remove_large(country_data[country]["indicators"]["other"]["health_workforce_perc_of_budget_latest"] * 100) for country in countries],
    )

    extra_context["graph_outpatient_visits"] = CountryBarGraph(
        countries,
        "graph_outpatient_visits",
        "Number of Outpatient Department Visits per 10,000 population",
        [country_data[country]["indicators"]["other"]["outpatient_visits_baseline"] for country in countries],
        [country_data[country]["indicators"]["other"]["outpatient_visits_latest"] for country in countries],
    )

    extra_context["graph_skilled_medical"] = TargetCountryBarGraph(
        countries,
        "graph_skilled_medical",
        "Number of skilled medical personnel per 10,000 population",
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

    class StackedAgencyBarGraph(DPChart):
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
                    "rotation" : -90,
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
                "color" : "#82A8A0"
            }, {
                "name" : dataset["name1"],
                "data" : data1,
                "color" : "#2D5352",
            }, {
                "name" : "Target = %s%%" % (target),
                "data" : [target] * len(categories),
                "type" : "line",
                "color" : "#F68B1F",
                "marker" : {
                    "enabled" : "false"
                },
            }]

            self.plotOptions = {"column" : {"stacking" : "percent"}}

    extra_context["graph_pfm"] = StackedAgencyBarGraph(
        "graph_pfm",
        "5DPb: Partner use of country public financial management systems",
        {
            "name1" : "Health aid using PFM systems (Q15)",
            "name2" : "Health aid not using PFM systems (Q14 - Q15)",
            "data" : indicator_data("5DPb", reverse=True)
        },
        "target", 80
    )
        
    extra_context["graph_procurement"] = StackedAgencyBarGraph(
        "graph_procurement",
        "5DPa: Partner use of country procurement systems",
        {
            "name1" : "Health aid using procurement systems (Q13)",
            "name2" : "Health aid not using procurement systems (Q12 - Q13)",
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
        "2DPC: Support provided as Programme Based Approach",
        {
            "name1" : "% of health aid as Programme Based Approach",
            "name2" : "% of health aid not as Programme Based Approach",
            "data" : indicator_data("2DPc")
        },
        "target", 66
    )

    extra_context["graph_tc"] = StackedAgencyBarGraph(
        "graph_tc",
        "2DPb: Support for capacity development that is coordinated <br/>and in line with national strategies",
        {
            "name1" : "Support coordinated and in line",
            "name2" : "Support not coordinated and in line",
            "data" : indicator_data("2DPb")
        },
        "target", 50
    )

    extra_context["graph_aob"] = StackedAgencyBarGraph(
        "graph_aob",
        "2DPa: Proportion of partner health aid on country budget",
        {
            "name2" : "Health aid not on budget",
            "name1" : "Health aid reported on budget",
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

    # TODO
    # Request from James to zero negative values
    neg_to_zero = lambda x : 0 if x < 0 else x


    # Nepal needs to be shown at the end of the list and with an asterix
    nepal = Country.objects.get(country="Nepal")
    nepal.country = nepal.country + "*"
    countries_3g = list(countries) + [nepal]
    countries_3g.remove(nepal)
    extra_context["graph_3G"] = TargetCountryBarGraph(
        countries_3g,
        "graph_3G",
        "3G: Proportion of national budget allocated to health",
        [data_3G[country][0][0] for country in countries_3g],
        [data_3G[country][0][2] for country in countries_3g],
        "Target", 15,
    )
    extra_context["graph_3G"].subtitle = {
            "text": '* Target for Nepal is 10%',
            "align": 'left',
            "x": 50,
            "y": 388,
            "floating" : "true",
        }

    extra_context["graph_4G"] = CountryBarGraph(
        countries,
        "graph_4G",
        "4G: Actual disbursement of government health budgets",
        [neg_to_zero(data_4G[country][0][0]) for country in countries],
        [neg_to_zero(data_4G[country][0][2]) for country in countries],
    )
    
    return direct_to_template(request, template=template_name, extra_context=extra_context)
