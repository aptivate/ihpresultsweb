from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist
from django.template import resolve_variable
from submissions.indicators import calc_agency_country_indicators

register = Library()

class AgencyCountryIndicatorNode(Node):
    def __init__(self, agency, country, out_var):
        self.agency = Variable(agency)
        self.country = Variable(country)
        self.out_var = out_var

    def render(self, context):
        try:
            agency = self.agency.resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('"agencycountryindicators" tag got an unknown variable: %r' % self.agency)

        try:
            country = self.country.resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('"agencycountryindicators" tag got an unknown variable: %r' % self.country)

        indicators = calc_agency_country_indicators(agency, country)
        context[self.out_var] = indicators
        return ""


def parse_agencycountryindicators(parser, token):
    """
    Create a new context variable that contains the indicators
    for an agency-country

    e.g.
    {% agencycountryindicators agency country as indicators %}

    """
    tokens = token.contents.split()
    if len(tokens) < 5:
        raise TemplateSyntaxError(u"'%r' tag requires 3 arguments." % tokens[0])
    if tokens[3] != "as":
        raise TemplateSyntaxError(u"'%r' usage: agencycountryindicators agency country as indicators" % tokens[0])
        
    return AgencyCountryIndicatorNode(tokens[1], tokens[2], tokens[4])

register.tag('agencycountryindicators', parse_agencycountryindicators)

