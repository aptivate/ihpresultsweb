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

def resolve_variable(variable, context):
    try:
        return variable.resolve(context)
    except VariableDoesNotExist:
        raise TemplateSyntaxError('tag got an unknown variable: %r' % variable)
    
class OverallGraphNode(Node):
    def __init__(self, element, baseline_value, latest_value, target_value, title, yaxis, xaxis):
        self.element = element
        self.baseline_value = Variable(baseline_value)
        self.latest_value = Variable(latest_value)
        self.target_value = Variable(target_value)
        self.title = Variable(title)
        self.yaxis = Variable(yaxis)
        self.xaxis = Variable(xaxis)

    def render(self, context):
        try:
            target_element = self.element
            baseline_value = ffloat(resolve_variable(self.baseline_value, context))
            latest_value = ffloat(resolve_variable(self.latest_value, context))
            target_value = resolve_variable(self.target_value, context)
            title = resolve_variable(self.title, context)
            yaxis = resolve_variable(self.yaxis, context)
            xaxis = resolve_variable(self.xaxis, context)

            var_name = "chart_%s" % (random.randint(0, 10000000))
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
                        xAxis: [{
                           categories: ["Baseline", "Latest"],
                           title : {
                                text: "%(xaxis)s"
                           },
                           showFirstLabel: false,
                           showLastLabel: false,
                        }, {
                           opposite: true,
                           labels: {
                                style: {
                                    display: 'None'
                                } 
                           },
                        }],
                        yAxis: {
                            title: {
                               text: "%(yaxis)s"
                            }
                        },
                        series: [{
                           name: 'baseline',
                           data: [%(baseline_value)s, %(latest_value)s],
                           xAxis: 0
                        }, {
                           type: 'line',
                           xAxis: 1,
                           name: 'Target',
                           data: [%(target_value)s, %(target_value)s],
                           dashStyle: 'shortDash',
                           marker: {
                               enabled: false
                           },
                           pointStart: -1,
                           pointInterval:3,
                        }],
                        tooltip : {
                            formatter: function() {
                                if (this.point.category == -1 || this.point.category == 2)
                                    return "Target: " + this.point.y + "%%";
                                return this.point.category + ": " + this.point.y + "%%";
                            }
                        }
                    });
                });
            """ % locals() 
            return s
        except:
            traceback.print_exc()

def parse_overall_graph(parser, token):
    """
    Output the javascript code for an overall graph

    e.g.
    {% overallgraph element baseline_value latest_value target_value title yaxis xaxis %}

    """
    tokens = token.contents.split()
    if len(tokens) != 8:
        raise TemplateSyntaxError(u"'%r' tag requires 7 arguments." % tokens[0])
        
    return OverallGraphNode(tokens[1], tokens[2], tokens[3], tokens[4], tokens[5], tokens[6], tokens[7])

register.tag('absgraph', parse_absolute_graph)
register.tag('ratiograph', parse_ratio_graph)
register.tag('overallgraph', parse_overall_graph)
