from collections import defaultdict
from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist
from django.template import resolve_variable
from submissions.indicators import calc_agency_country_indicators, NA_STR
import traceback
import random

register = Library()

def ffloat(x):
    if x == None: return "0"
    try:
        x = float(x)
        return "%.1f" % x
    except:
        return "0"

class AbsGraphNode(Node):
    def __init__(self, agency, indicator, data, element, title, yaxis, xaxis):
        self.agency = Variable(agency)
        self.indicator = indicator
        self.data = Variable(data)
        self.element = element
        self.title = Variable(title)
        self.yaxis = Variable(yaxis)
        self.xaxis = Variable(xaxis)

    def render(self, context):
        try:
            try:
                agency = self.agency.resolve(context)
            except VariableDoesNotExist:
                raise TemplateSyntaxError('"absgraph" tag got an unknown variable: %r' % self.agency)

            try:
                data = self.data.resolve(context)
            except VariableDoesNotExist:
                raise TemplateSyntaxError('"absgraph" tag got an unknown variable: %r' % self.data)

            try:
                title = self.title.resolve(context)
            except VariableDoesNotExist:
                raise TemplateSyntaxError('"absgraph" tag got an unknown variable: %r' % self.title)

            try:
                yaxis = self.yaxis.resolve(context)
            except VariableDoesNotExist:
                raise TemplateSyntaxError('"absgraph" tag got an unknown variable: %r' % self.yaxis)

            try:
                xaxis = self.xaxis.resolve(context)
            except VariableDoesNotExist:
                raise TemplateSyntaxError('"absgraph" tag got an unknown variable: %r' % self.xaxis)


            countries_list = ",".join('"%s"' % country for country, _ in data)
            baseline_vals = ",".join(ffloat(datum[self.indicator][0]) for country, datum in data)
            latest_vals = ",".join(ffloat(datum[self.indicator][1]) for country, datum in data)
            var_name = "chart_%s" % (random.randint(0, 10000000))
            target_element = self.element
            indicator = self.indicator

            s = """
                var %(var_name)s; // globally available
                $(document).ready(function() {
                    %(var_name)s = new Highcharts.Chart({
                        chart: {
                            renderTo: '%(target_element)s',
                            defaultSeriesType: 'column'
                        },
                        title: {
                           text: "%(title)s"
                        },
                        xAxis: {
                           categories: [%(countries_list)s],
                            title : {
                                text: "%(xaxis)s"
                            }
                        },
                        yAxis: {
                            title: {
                               text: "%(yaxis)s"
                            }
                        },
                        series: [{
                           name: 'baseline',
                           data: [%(baseline_vals)s]
                        }, {
                           name: 'latest',
                           data: [%(latest_vals)s]
                        }]
                    });
                });
            """ % locals()
            return s
        except:
            traceback.print_exc()

class RatioGraphNode(Node):
    def __init__(self, agency, indicator, data, element, title, yaxis, xaxis):
        self.agency = Variable(agency)
        self.indicator = indicator
        self.data = Variable(data)
        self.element = element
        self.title = Variable(title)
        self.yaxis = Variable(yaxis)
        self.xaxis = Variable(xaxis)

    def render(self, context):
        try:
            try:
                agency = self.agency.resolve(context)
            except VariableDoesNotExist:
                raise TemplateSyntaxError('"absgraph" tag got an unknown variable: %r' % self.agency)

            try:
                data = self.data.resolve(context)
            except VariableDoesNotExist:
                raise TemplateSyntaxError('"absgraph" tag got an unknown variable: %r' % self.data)

            try:
                title = self.title.resolve(context)
            except VariableDoesNotExist:
                raise TemplateSyntaxError('"absgraph" tag got an unknown variable: %r' % self.title)

            try:
                yaxis = self.yaxis.resolve(context)
            except VariableDoesNotExist:
                raise TemplateSyntaxError('"absgraph" tag got an unknown variable: %r' % self.yaxis)

            try:
                xaxis = self.xaxis.resolve(context)
            except VariableDoesNotExist:
                raise TemplateSyntaxError('"absgraph" tag got an unknown variable: %r' % self.xaxis)

            countries_list = ",".join('"%s"' % country for country, _ in data)
            data_vals = ",".join(ffloat(datum[self.indicator]) for country, datum in data)
            var_name = "chart_%s" % (random.randint(0, 10000000))
            target_element = self.element
            indicator = self.indicator

            s = """
                var %(var_name)s; // globally available
                $(document).ready(function() {
                    %(var_name)s = new Highcharts.Chart({
                        chart: {
                            renderTo: '%(target_element)s',
                            defaultSeriesType: 'column'
                        },
                        title: {
                           text: "%(title)s"
                        },
                        xAxis: {
                           categories: [%(countries_list)s],
                            title : {
                                text: "%(xaxis)s"
                            }
                        },
                        yAxis: {
                            title: {
                               text: "%(yaxis)s"
                            }
                        },
                        series: [{
                           name: 'data',
                           data: [%(data_vals)s]
                        }]
                    });
                });
            """ % locals() 
            return s
        except:
            traceback.print_exc()

def parse_absolute_graph(parser, token):
    """
    Output the javascript code for an absgraph

    e.g.
    {% absgraph agency indicator data element %}

    """
    tokens = token.contents.split()
    print tokens, len(tokens)
    if len(tokens) != 8:
        raise TemplateSyntaxError(u"'%r' tag requires 7 arguments." % tokens[0])
        
    return AbsGraphNode(tokens[1], tokens[2], tokens[3], tokens[4], tokens[5], tokens[6], tokens[7])

def parse_ratio_graph(parser, token):
    """
    Output the javascript code for a ratiograph

    e.g.
    {% ratiograph agency indicator data element %}

    """
    tokens = token.contents.split()
    if len(tokens) != 8:
        raise TemplateSyntaxError(u"'%r' tag requires 7 arguments." % tokens[0])
        
    return RatioGraphNode(tokens[1], tokens[2], tokens[3], tokens[4], tokens[5], tokens[6], tokens[7])

def resolve_variable(variable, context):
    try:
        return variable.resolve(context)
    except VariableDoesNotExist:
        raise TemplateSyntaxError('tag got an unknown variable: %r' % variable)

class CountryBarGraphNode(Node):
    def __init__(self, element, data):
        self.element = element
        self.data = Variable(data)

    def render(self, context):
        try:
            target_element = self.element
            data = resolve_variable(self.data, context)

            title = data["title"]
            y_axis = data.get("y-axis", "%")
            
            values = data["data"]
            countries = ",".join('"%s"' % el for el in values.keys())
            baseline_data = ",".join(ffloat(el["baseline"]) for el in values.values())
            latest_data = ",".join(ffloat(el["latest"]) for el in values.values())

            if "target" in data:
                target_name = data["target"].get("name", "Target")
                target_value = data["target"]["value"]
                target_data = ",".join(ffloat(target_value) for el in values.keys())
                target_series = """ {
                           type: 'line',
                           color: '#ff0000',
                           name: '%(target_name)s',
                           data: [%(target_data)s],
                           marker: {
                               enabled: false
                           },
                        }""" % locals()
            else:
                target_series = ""


            var_name = "chart_%s" % (random.randint(0, 10000000))
            s = """
                var %(var_name)s; // globally available
                $(document).ready(function() {
                    %(var_name)s = new Highcharts.Chart({
                        chart: {
                            renderTo: '%(target_element)s',
                            defaultSeriesType: 'column',
                            marginTop: 50,
                        },
                        title: {
                           text: "%(title)s"
                        },
                        xAxis: {
                           categories: [%(countries)s]
                        },
                        yAxis: {
                            title: {
                               text: "%(y_axis)s"
                            }
                        },
                        series: [{
                           name: 'Baseline',
                           data: [%(baseline_data)s],
                        }, {
                           name: '2009',
                           data: [%(latest_data)s],
                        }, %(target_series)s ],
                    });
                });
            """ % locals() 
            return s
        except:
            traceback.print_exc()

class Series(object):
    def __init__(self, data):
        self.data = data

    def _format(self, v):
        if type(v) == str:
            if v == "false" or v == "true":
                return v
            return "'%s'" % v
        elif type(v) == list or type(v) == tuple:
            return "[" + ",".join(self._format(i) for i in v) + "]"
        elif type(v) == int:
            return str(v)
        elif type(v) == float:
            return ffloat(v)
        elif type(v) == dict:
            return str(Series(v))

    def __str__(self):
        return "{" + ",".join(["%s : %s" % (k, self._format(v)) for (k, v) in self.data.items()]) + "}"

class StackedBarGraph(Node):
    def __init__(self, element, data):
        self.element = element
        self.data = Variable(data)

    def render(self, context):
        try:
            target_element = self.element
            data = resolve_variable(self.data, context)

            title = data["title"]
            y_axis = data.get("y-axis", "%")
            
            values = data["data"]
            keys = [key for key, _ in values]
            categories = ",".join('"%s"' % el for el in keys)

            data_series = zip(*[k for _, k in values])
            series_labels = data["series"]
            data_series = zip(series_labels, data_series)

            series = []
            for series_name, series_data in data_series:
                series.append(Series({
                    "data" : series_data,
                    "name" : series_name,
                }))

            if "target" in data:
                target_value = data["target"]["value"]
                series.append(Series({
                    "name" : data["target"].get("name", "Target"),
                    "color": '#ff0000',
                    "data" : [target_value] * len(values),
                    "marker" : { "enabled" : "false" },
                    "type" : "line",
                }))

            series_text = ",\n".join(str(s) for s in series)


            var_name = "chart_%s" % (random.randint(0, 10000000))
            s = """
                var %(var_name)s; // globally available
                $(document).ready(function() {
                    %(var_name)s = new Highcharts.Chart({
                        chart: {
                            renderTo: '%(target_element)s',
                            defaultSeriesType: 'column',
                            marginTop: 50,
                        },
                        title: {
                           text: "%(title)s"
                        },
                        xAxis: {
                           categories: [%(categories)s]
                        },
                        yAxis: {
                            title: {
                               text: "%(y_axis)s"
                            }
                        },
                        plotOptions : {
                            column: {
                                stacking: 'percent'
                            }
                        },
                        series: [%(series_text)s]
                    });
                });
            """ % locals() 
            return s
        except:
            traceback.print_exc()

def parse_countrybar_graph(parser, token):
    """
    Output the javascript code for a country bar graph

    e.g.
    {% countrybargraph element data %}

    """
    tokens = token.contents.split()
    if len(tokens) != 3:
        raise TemplateSyntaxError(u"'%r' tag requires 2 arguments." % tokens[0])
        
    return CountryBarGraphNode(tokens[1], tokens[2])

def parse_stacked_graph(parser, token):
    """
    Output the javascript code for a stacked bar graph

    e.g.
    {% stackedbargraph element data %}

    """
    tokens = token.contents.split()
    if len(tokens) != 3:
        raise TemplateSyntaxError(u"'%r' tag requires 2 arguments." % tokens[0])
        
    return StackedBarGraph(tokens[1], tokens[2])

register.tag('absgraph', parse_absolute_graph)
register.tag('ratiograph', parse_ratio_graph)
register.tag('countrybargraph', parse_countrybar_graph)
register.tag('stackedbargraph', parse_stacked_graph)
