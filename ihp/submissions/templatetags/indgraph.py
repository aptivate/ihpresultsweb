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

register.tag('absgraph', parse_absolute_graph)
register.tag('ratiograph', parse_ratio_graph)
