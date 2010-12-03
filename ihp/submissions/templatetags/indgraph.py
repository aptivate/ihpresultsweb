from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist
from django.template import resolve_variable
from submissions.indicators import calc_agency_country_indicators, NA_STR
import traceback
import random

register = Library()

def ffloat(x):
    if x == None: return "0"
    if not type(x) == float: return "0"
    return "%.1f" % x

class AbsGraphNode(Node):
    def __init__(self, agency, indicator, data, element):
        self.agency = Variable(agency)
        self.indicator = indicator
        self.data = Variable(data)
        self.element = element

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

            countries_list = ",".join('"%s"' % country for country, _ in data)
            baseline_vals = ",".join(ffloat(datum[self.indicator][0]) for country, datum in data)
            latest_vals = ",".join(ffloat(datum[self.indicator][1]) for country, datum in data)
            var_name = "chart_%s" % (random.randint(0, 10000000))
            s = """
                var %s; // globally available
                $(document).ready(function() {
                    %s = new Highcharts.Chart({
                        chart: {
                            renderTo: '%s',
                            defaultSeriesType: 'column'
                        },
                        title: {
                           text: '%s'
                        },
                        xAxis: {
                           categories: [%s],
                        },
                        yAxis: {
                            title: {
                               text: '%%'
                            }
                        },
                        series: [{
                           name: 'baseline',
                           data: [%s]
                        }, {
                           name: 'latest',
                           data: [%s]
                        }]
                    });
                });
            """ % (var_name, var_name, self.element, self.indicator, countries_list, baseline_vals, latest_vals)
            return s
        except:
            traceback.print_exc()

class RatioGraphNode(Node):
    def __init__(self, agency, indicator, data, element):
        self.agency = Variable(agency)
        self.indicator = indicator
        self.data = Variable(data)
        self.element = element

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

            countries_list = ",".join('"%s"' % country for country, _ in data)
            data_vals = ",".join(ffloat(datum[self.indicator]) for country, datum in data)
            var_name = "chart_%s" % (random.randint(0, 10000000))
            s = """
                var %s; // globally available
                $(document).ready(function() {
                    %s = new Highcharts.Chart({
                        chart: {
                            renderTo: '%s',
                            defaultSeriesType: 'column'
                        },
                        title: {
                           text: '%s'
                        },
                        xAxis: {
                           categories: [%s],
                        },
                        yAxis: {
                            title: {
                               text: '%%'
                            }
                        },
                        series: [{
                           name: 'data',
                           data: [%s]
                        }]
                    });
                });
            """ % (var_name, var_name, self.element, self.indicator, countries_list, data_vals)
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
    if len(tokens) != 5:
        raise TemplateSyntaxError(u"'%r' tag requires 4 arguments." % tokens[0])
        
    return AbsGraphNode(tokens[1], tokens[2], tokens[3], tokens[4])

def parse_ratio_graph(parser, token):
    """
    Output the javascript code for a ratiograph

    e.g.
    {% ratiograph agency indicator data element %}

    """
    tokens = token.contents.split()
    if len(tokens) != 5:
        raise TemplateSyntaxError(u"'%r' tag requires 4 arguments." % tokens[0])
        
    return RatioGraphNode(tokens[1], tokens[2], tokens[3], tokens[4])

register.tag('absgraph', parse_absolute_graph)
register.tag('ratiograph', parse_ratio_graph)
