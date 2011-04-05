from django.views.generic.simple import direct_to_template
from functools import partial
from submissions.models import Agency, Country
from indicators import calc_agency_country_indicators, NA_STR, calc_overall_agency_indicators, positive_funcs, calc_country_indicators
from highcharts import Chart, ChartObject
import country_scorecard
import agency_scorecard
import translations
import models

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
    def __init__(self, target_element, source, **kwargs):
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
    
        self.chart = {}
        for key in kwargs:
            setattr(self, key, kwargs[key])

        if "title" in kwargs:
            title = kwargs["title"]
            self.title = {"text" : title}

            if "<br" in title:
                self.chart["marginTop"] = 50

        if "subtitle" in kwargs:
            self.subtitle = {
                "text": kwargs["subtitle"],
                "align": 'left',
                "x": 50,
                "y": 388,
                "floating" : "true",
            }
        if "yAxis" in kwargs:
            self.yAxis = {"title" : {"text" : kwargs["yAxis"]}} 
            if "<br" in kwargs["yAxis"]:
                self.yAxis["title"]["margin"] = 40


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
    def __init__(self, target_element, **kwargs):
        source = kwargs.get("source", "Source: DP data returns")
        super(DPChart, self).__init__(target_element, source, **kwargs)

class CountryChart(IHPChart):
    def __init__(self, target_element, **kwargs):
        source = kwargs.get("source", "Source: Country data returns/CSO data returns")
        super(CountryChart, self).__init__(target_element, source, **kwargs)

class StackedAgencyBarGraph(DPChart):
    def __init__(self, chart_name, dataset, target_name, target, **kwargs):
        kwargs["yAxis"] = "%"
        super(StackedAgencyBarGraph, self).__init__(chart_name, **kwargs)
        categories = map(lambda x: x[0].agency, dataset["data"])
        data = map(lambda x: x[1], dataset["data"])

        data1 = data
        data2 = map(lambda x: 100 - x, data)

        self.chart["defaultSeriesType"] = "column"
        self.xAxis = {
            "categories" : categories,
            "labels" : {
                "rotation" : -90,
                "y" : 40,
            }
        } 

        if hasattr(self, "yAxis"):
            self.yAxis["max"] = 100

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

class AgencyBarGraph(DPChart):
    def __init__(self, agencies, chart_name, series, **kwargs):
        agency_names = map(lambda x: x.agency, agencies)

        super(AgencyBarGraph, self).__init__(chart_name, **kwargs)
        self.chart["defaultSeriesType"] = "column"
        
        self.xAxis = {
            "categories" : agency_names,
            "labels" : {
                "rotation" : -90,
                "y" : 40,
            }
        } 

        if type(series) != list:
            series = [series]
        self.series = series

class CountryBarGraph(CountryChart):
    def __init__(self, countries, chart_name, baseline_data, latest_data, **kwargs):
        country_names = map(lambda x: x.country, countries)
        kwargs["yAxis"] = "%"

        super(CountryBarGraph, self).__init__(chart_name, **kwargs)
        self.chart["defaultSeriesType"] = "column"
        
        country_names = [country.country for country in countries]
        self.xAxis = {
            "categories" : country_names,
            "labels" : {
                "rotation" : -90,
                "y" : 40,
            }
        } 
        self.series = [{
            "name" : "Baseline",
            "data" : baseline_data
        }, {
            "name" : "2009",
            "data" : latest_data 
        }]

class AgencyCountryBarGraph(DPChart):
    def __init__(self, countries, chart_name, baseline_data, latest_data, **kwargs):
        super(AgencyCountryBarGraph, self).__init__(chart_name, **kwargs)

        country_names = map(lambda x: x.country, countries)
        self.chart["defaultSeriesType"] = "column"
        country_names = [country.country for country in countries]
        self.xAxis = {
            "categories" : country_names,
            "labels" : {
                "rotation" : -90,
                "y" : 40,
            }
        } 

        self.series = [{
            "name" : "Baseline",
            "data" : baseline_data 
        }, {
            "name" : "2009",
            "data" : latest_data 
        }]

class AgencyCountryLatestBarGraph(AgencyCountryBarGraph):
    def __init__(self, countries, chart_name, latest_data, **kwargs):
        super(AgencyCountryLatestBarGraph, self).__init__(countries, chart_name, [], latest_data, **kwargs)

        self.series = [{
            "name" : "% change from baseline year",
            "data" : latest_data 
        }]

class CountryAgencyBarGraph(DPChart):
    def __init__(self, agencies, chart_name, baseline_data, latest_data, **kwargs):
        super(CountryAgencyBarGraph, self).__init__(chart_name, **kwargs)

        agency_names = map(lambda x: x.agency, agencies)
        self.chart["defaultSeriesType"] = "column"
        self.xAxis = {
            "categories" : agency_names,
            "labels" : {
                "rotation" : -90,
                "y" : 40,
            }
        } 

        self.series = [{
            "name" : "Baseline",
            "data" : baseline_data 
        }, {
            "name" : "2009",
            "data" : latest_data 
        }]

class CountryAgencyLatestBarGraph(CountryAgencyBarGraph):
    def __init__(self, agencies, chart_name, latest_data, **kwargs):
        super(CountryAgencyLatestBarGraph, self).__init__(agencies, chart_name, [], latest_data, **kwargs)

        self.series = [{
            "name" : "2009",
            "data" : latest_data 
        }]

class TargetCountryBarGraph(CountryBarGraph):
    def __init__(self, countries, chart_name, baseline_data, latest_data, target_name, target, **kwargs):
        super(TargetCountryBarGraph, self).__init__(countries, chart_name, baseline_data, latest_data, **kwargs)
        self.series.append({
            "name" : target_name,
            "data" : [target] * len(latest_data),
            "type" : "line",
            "color" : "#F68B1F",
            "marker" : {
                "enabled" : "false"
            },
        })

class HighlevelBarChart(DPChart):
    def __init__(self, target_element, baseline_value, latest_value, **kwargs):
        super(HighlevelBarChart, self).__init__(target_element, **kwargs)

        self.xAxis = {"categories" : ["Baseline", "2009"]} 

        self.series = [{
            "name" : "Aggregated Data",
            "type" : "column",
            "data" : [float(baseline_value), float(latest_value)],
            "color" : '#82A8A0',
        }]

        if "target" in kwargs:
            self.series.append({
                "type" : "line",
                "name" : "Target",
                "data" : [kwargs["target"]] * 2,
                "dashStyle" : "shortDash",
                "marker" : {
                    "enabled" : "false"
                },
                "color": "#F68B1F",
            })

def agency_graphs_by_indicator(request, indicator, language, template_name="submissions/agency_graphs_by_indicator.html", extra_context=None):
    extra_context = extra_context or {}
    translation = request.translation

    indicators = calc_overall_agency_indicators(funcs=positive_funcs)

    extra_context["graphs"] = graphs = []
    name = "graph_%s" % indicator

    (baseline_value, baseline_year, latest_value, latest_year) = indicators[indicator][0]
    target = target_values[indicator]
    graph = highlevel_graph_by_indicator(indicator, name, translation, baseline_value, latest_value, target=target)
    graphs.append({
        "name" : name,
        "obj" : graph
    })

    agency_data = dict([(agency, agency_scorecard.get_agency_scorecard_data(agency)) for agency in Agency.objects.all()])

    name = "graph2_%s" % indicator
    graph = additional_graph_by_indicator(indicator, name, translation, agency_data)
    graphs.append({
        "name" : name,
        "obj" : graph
    })

    return direct_to_template(request, template=template_name, extra_context=extra_context)

def projectiongraphs(request, language, template_name="submissions/projectiongraphs.html", extra_context=None):
    extra_context = extra_context or {}

    translation = request.translation

    indicators = calc_overall_agency_indicators(funcs=positive_funcs)

    for indicator in ["2DPa", "5DPb"]:
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

        graph.title = {"text" : translation.projection_graphs[indicator]["title"]}
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
            "name": translation.target_language["target"],
            "data": target_data,
            "marker": {
               "enabled": "false"
            },
        }]

        extra_context["graph_%s" % indicator] = graph 

    return direct_to_template(request, template=template_name, extra_context=extra_context)

def highlevel_graph_by_indicator(indicator, name, translation, baseline_value, latest_value, target=None):

    if target:
        graph = HighlevelBarChart(
            name, 
            float(baseline_value), float(latest_value),
            title=translation.highlevel_graphs[indicator]["title"],
            subtitle=translation.highlevel_graphs[indicator]["subtitle"],
            target=target_values[indicator],
            yAxis=translation.highlevel_graphs[indicator]["yAxis"],
        )
    else:
        graph = HighlevelBarChart(
            name, 
            float(baseline_value), float(latest_value),
            title=translation.highlevel_graphs[indicator]["title"],
            subtitle=translation.highlevel_graphs[indicator]["subtitle"],
            yAxis=translation.highlevel_graphs[indicator]["yAxis"],
        )

    graph.legend = {
        "enabled" : "false"
    }

    return graph

def additional_graph_by_indicator(indicator, name, translation, agency_data):

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

    target = target_values[indicator]

    if indicator == "5DPc":
        data = indicator_data(indicator)
        agencies = [datum[0] for datum in data]
        series = {
            "name" : "PIUs",
            "data" : [datum[1] for datum in data]
        }
        graph = AgencyBarGraph(
            agencies, name, series,
            title=translation.additional_graphs[indicator]["title"],
            yAxis=translation.additional_graphs[indicator]["yAxis"],
            legend={"enabled" : "false"},
        )
        return graph

    else:
        reverse = ["2DPa", "5DPa", "5DPb"]
        return StackedAgencyBarGraph(
            name,
            {
                "name1" : translation.additional_graphs[indicator]["series1"],
                "name2" : translation.additional_graphs[indicator]["series2"],
                "data" : indicator_data(indicator, reverse=True if indicator in reverse else False)
            },
            "target", target,
            title=translation.additional_graphs[indicator]["title"]
        )

def highlevelgraphs(request, language, template_name="submissions/highlevelgraphs.html", extra_context=None, titles=None):
    extra_context = extra_context or {}

    translation = request.translation
    indicators = calc_overall_agency_indicators(funcs=positive_funcs)

    for indicator in indicators:
        (baseline_value, _, latest_value, _) = indicators[indicator][0]
        name = "graph_%s" % indicator.lower()
        if indicator not in ["5DPc"]:
            graph = highlevel_graph_by_indicator(indicator, name, translation, baseline_value, latest_value, target_values[indicator])
        else:
            graph = highlevel_graph_by_indicator(indicator, name, translation, baseline_value, latest_value)

        extra_context["graph_%s" % indicator] = graph 

    agency_data = dict([(agency, agency_scorecard.get_agency_scorecard_data(agency)) for agency in Agency.objects.all()])

    extra_context["graph_pfm"] = additional_graph_by_indicator("5DPb", "graph_pfm", translation, agency_data)
    extra_context["graph_procurement"] = additional_graph_by_indicator("5DPa", "graph_procurement", translation, agency_data)
    extra_context["graph_multi_year"] = additional_graph_by_indicator("3DP", "graph_multi_year", translation, agency_data)
    extra_context["graph_pba"] = additional_graph_by_indicator("2DPc", "graph_pba", translation, agency_data)
    extra_context["graph_tc"] = additional_graph_by_indicator("2DPb", "graph_tc", translation, agency_data)
    extra_context["graph_aob"] = additional_graph_by_indicator("2DPa", "graph_aob", translation, agency_data)

    return direct_to_template(request, template=template_name, extra_context=extra_context)

def calc_graph_values(indicator, base_val, latest_val):
    if indicator in ["2DPa", "5DPa", "5DPb"]:
        return None, safe_mul(safe_div(safe_diff(latest_val, base_val), base_val), 100)
    else:
        return base_val, latest_val

def agencygraphs(request, agency_name, language=None, template_name="submissions/agencygraphs.html", extra_context=None):
    extra_context = extra_context or {}

    agency = Agency.objects.get(agency__iexact=agency_name)
    extra_context["translation"] = translation = request.translation

    data = {}
    for country in agency.countries:
        country_data = {}
        indicators = calc_agency_country_indicators(agency, country)
        for indicator in ["2DPa", "2DPb", "2DPc", "3DP", "4DP", "5DPa", "5DPb", "5DPc"]:
            base_val, _, latest_val, _ = indicators[indicator][0]
            country_data[indicator] = calc_graph_values(indicator, base_val, latest_val)
        data[country.country] = country_data
    
    agency_name = agency.agency

    extra_context["graph_2DPa"] = AgencyCountryLatestBarGraph(
        agency.countries, "graph_2DPa", 
        [data[country.country]["2DPa"][1] for country in agency.countries],
        title=translation.agency_graphs["2DPa"]["title"] % locals(),
        yAxis=translation.agency_graphs["2DPa"]["yAxis"],
    )

    extra_context["graph_2DPb"] = AgencyCountryBarGraph(
        agency.countries, "graph_2DPb",
        [data[country.country]["2DPb"][0] for country in agency.countries],
        [data[country.country]["2DPb"][1] for country in agency.countries],
        title=translation.agency_graphs["2DPb"]["title"] % locals(),
        yAxis=translation.agency_graphs["2DPb"]["yAxis"],
    )

    extra_context["graph_2DPc"] = AgencyCountryBarGraph(
        agency.countries, "graph_2DPc",
        [data[country.country]["2DPc"][0] for country in agency.countries],
        [data[country.country]["2DPc"][1] for country in agency.countries],
        title=translation.agency_graphs["2DPc"]["title"] % locals(),
        yAxis=translation.agency_graphs["2DPc"]["yAxis"],
    )

    extra_context["graph_3DP"] = AgencyCountryBarGraph(
        agency.countries, "graph_3DP",
        [data[country.country]["3DP"][0] for country in agency.countries],
        [data[country.country]["3DP"][1] for country in agency.countries],
        title=translation.agency_graphs["3DP"]["title"],
        yAxis=translation.agency_graphs["3DP"]["yAxis"],
    )

    extra_context["graph_4DP"] = AgencyCountryBarGraph(
        agency.countries, "graph_4DP",
        [data[country.country]["4DP"][0] for country in agency.countries],
        [data[country.country]["4DP"][1] for country in agency.countries],
        title=translation.agency_graphs["4DP"]["title"] % agency.agency,
        yAxis=translation.agency_graphs["4DP"]["yAxis"],
    )

    extra_context["graph_5DPa"] = AgencyCountryLatestBarGraph(
        agency.countries, "graph_5DPa",
        [data[country.country]["5DPa"][1] for country in agency.countries],
        title=translation.agency_graphs["5DPa"]["title"],
        yAxis=translation.agency_graphs["5DPa"]["yAxis"],
    )

    extra_context["graph_5DPb"] = AgencyCountryLatestBarGraph(
        agency.countries, "graph_5DPb",
        [data[country.country]["5DPb"][1] for country in agency.countries],
        title=translation.agency_graphs["5DPb"]["title"] % agency.agency,
        yAxis=translation.agency_graphs["5DPb"]["yAxis"],
    )

    extra_context["graph_5DPc"] = AgencyCountryBarGraph(
        agency.countries, "graph_5DPc",
        [data[country.country]["5DPc"][0] for country in agency.countries],
        [data[country.country]["5DPc"][1] for country in agency.countries],
        title=translation.agency_graphs["5DPc"]["title"] % agency.agency,
        yAxis=translation.agency_graphs["5DPc"]["yAxis"],
    )
    
    return direct_to_template(request, template=template_name, extra_context=extra_context)
    
    
def countrygraphs(request, country_name, language, template_name="submissions/countrygraphs.html", extra_context=None):
    extra_context = extra_context or {}

    translation = request.translation
    country = Country.objects.get(country__iexact=country_name)
    
    data = {}
    for agency in country.agencies:
        agency_data = {}
        indicators = calc_agency_country_indicators(agency, country)
        for indicator in ["2DPa", "2DPb", "2DPc", "3DP", "4DP", "5DPa", "5DPb", "5DPc"]:
            base_val, _, latest_val, _ = indicators[indicator][0]
            agency_data[indicator] = calc_graph_values(indicator, base_val, latest_val)
        data[agency.agency] = agency_data

    country_name = country.country
    extra_context["graph_2DPa"] = CountryAgencyLatestBarGraph(
        country.agencies, "graph_2DPa", 
        [data[agency.agency]["2DPa"][1] for agency in country.agencies],
        title=translation.country_graphs["2DPa"]["title"] % locals(),
        yAxis=translation.country_graphs["2DPa"]["yAxis"] % locals(),
    )

    extra_context["graph_2DPb"] = CountryAgencyBarGraph(
        country.agencies, "graph_2DPb",
        [data[agency.agency]["2DPb"][0] for agency in country.agencies],
        [data[agency.agency]["2DPb"][1] for agency in country.agencies],
        title=translation.country_graphs["2DPb"]["title"] % locals(),
        yAxis=translation.country_graphs["2DPb"]["yAxis"] % locals(),
    )

    extra_context["graph_2DPc"] = CountryAgencyBarGraph(
        country.agencies, "graph_2DPc",
        [data[agency.agency]["2DPc"][0] for agency in country.agencies],
        [data[agency.agency]["2DPc"][1] for agency in country.agencies],
        title=translation.country_graphs["2DPc"]["title"] % locals(),
        yAxis=translation.country_graphs["2DPc"]["yAxis"] % locals(),
    )

    extra_context["graph_3DP"] = CountryAgencyBarGraph(
        country.agencies, "graph_3DP",
        [data[agency.agency]["3DP"][0] for agency in country.agencies],
        [data[agency.agency]["3DP"][1] for agency in country.agencies],
        title=translation.country_graphs["3DP"]["title"] % locals(),
        yAxis=translation.country_graphs["3DP"]["yAxis"] % locals(),
    )

    extra_context["graph_4DP"] = CountryAgencyBarGraph(
        country.agencies, "graph_4DP",
        [data[agency.agency]["4DP"][0] for agency in country.agencies],
        [data[agency.agency]["4DP"][1] for agency in country.agencies],
        title=translation.country_graphs["4DP"]["title"] % locals(),
        yAxis=translation.country_graphs["4DP"]["yAxis"] % locals(),
    )

    extra_context["graph_5DPa"] = CountryAgencyLatestBarGraph(
        country.agencies, "graph_5DPa",
        [data[agency.agency]["5DPa"][1] for agency in country.agencies],
        title=translation.country_graphs["5DPa"]["title"] % locals(),
        yAxis=translation.country_graphs["5DPa"]["yAxis"] % locals(),
    )

    extra_context["graph_5DPb"] = CountryAgencyLatestBarGraph(
        country.agencies, "graph_5DPb",
        [data[agency.agency]["5DPb"][1] for agency in country.agencies],
        title=translation.country_graphs["5DPb"]["title"] % locals(),
        yAxis=translation.country_graphs["5DPb"]["yAxis"] % locals(),
    )

    extra_context["graph_5DPc"] = CountryAgencyBarGraph(
        country.agencies, "graph_5DPc",
        [data[agency.agency]["5DPc"][0] for agency in country.agencies],
        [data[agency.agency]["5DPc"][1] for agency in country.agencies],
        title=translation.country_graphs["5DPc"]["title"] % locals(),
        yAxis=translation.country_graphs["5DPc"]["yAxis"] % locals(),
    )
    
    return direct_to_template(request, template=template_name, extra_context=extra_context)

    
def government_graphs(request, language, template_name="submission/country_graphs_by_indicator.html", extra_context=None):
    extra_context = extra_context or {}

    translation = request.translation

    countries = sorted(Country.objects.all(), key=lambda x: x.country)
    data_3G = dict([(c, calc_country_indicators(c)["3G"]) for c in countries])
    data_4G = dict([(c, calc_country_indicators(c)["4G"]) for c in countries])

    country_data = dict([(country, country_scorecard.get_country_export_data(country)) for country in Country.objects.all()])

    # TODO
    # Request from James to zero negative values
    neg_to_zero = lambda x : 0 if x < 0 else x

    # TODO
    # Request from James to remove overly large values
    remove_large = lambda x : 0 if x > 100 else x


    # Nepal needs to be shown at the end of the list and with an asterix
    nepal = Country.objects.get(country="Nepal")
    nepal.country = nepal.country + "*"
    countries_3g = list(countries) + [nepal]
    countries_3g.remove(nepal)
    extra_context["graph_3G"] = TargetCountryBarGraph(
        countries_3g,
        "graph_3G",
        [data_3G[country][0][0] for country in countries_3g],
        [data_3G[country][0][2] for country in countries_3g],
        translation.target_language["target"], 15,
        title=translation.government_graphs["3G"]["title"],
    )
    extra_context["graph_3G"].subtitle = {
        "text": translation.government_graphs["3G"]["subtitle"],
        "align": 'left',
        "x": 50,
        "y": 388,
        "floating" : "true",
    }

    extra_context["graph_4G"] = CountryBarGraph(
        countries,
        "graph_4G",
        [neg_to_zero(data_4G[country][0][0]) for country in countries],
        [neg_to_zero(data_4G[country][0][2]) for country in countries],
        title=translation.government_graphs["4G"]["title"],
    )

    extra_context["graph_hw"] = CountryBarGraph(
        countries,
        "graph_hw",
        [remove_large(country_data[country]["indicators"]["other"]["health_workforce_perc_of_budget_baseline"] * 100) for country in countries],
        [remove_large(country_data[country]["indicators"]["other"]["health_workforce_perc_of_budget_latest"] * 100) for country in countries],
        title=translation.government_graphs["health_workforce"]["title"],
    )

    extra_context["graph_outpatient_visits"] = CountryBarGraph(
        countries,
        "graph_outpatient_visits",
        [country_data[country]["indicators"]["other"]["outpatient_visits_baseline"] for country in countries],
        [country_data[country]["indicators"]["other"]["outpatient_visits_latest"] for country in countries],
        title=translation.government_graphs["outpatient_visits"]["title"],
    )
    extra_context["graph_outpatient_visits"].yAxis = {"title" : {"text" : ""}} 

    extra_context["graph_skilled_medical"] = TargetCountryBarGraph(
        countries,
        "graph_skilled_medical",
        [country_data[country]["indicators"]["other"]["skilled_personnel_baseline"] for country in countries],
        [country_data[country]["indicators"]["other"]["skilled_personnel_latest"] for country in countries],
        translation.target_language["who"], 23,
        title=translation.government_graphs["skilled_medical"]["title"],
    )
    extra_context["graph_skilled_medical"].yAxis = {"title" : {"text" : ""}} 

    extra_context["graph_health_budget"] = TargetCountryBarGraph(
        countries,
        "graph_health_budget",
        [country_data[country]["indicators"]["3G"]["baseline_value"] for country in countries],
        [country_data[country]["indicators"]["3G"]["latest_value"] for country in countries],
        translation.target_language["target"], 15,
        title=translation.government_graphs["health_budget"]["title"],
    )
    
    return direct_to_template(request, template=template_name, extra_context=extra_context)
