from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist
from django.template import resolve_variable
from submissions.indicators import calc_agency_country_indicators, NA_STR
import traceback

register = Library()

class AgencyCountryIndicatorNode(Node):
    def __init__(self, agency, country, out_var):
        self.agency = Variable(agency)
        self.country = Variable(country)
        self.out_var = out_var

    def render(self, context):
        try:
            try:
                agency = self.agency.resolve(context)
            except VariableDoesNotExist:
                raise TemplateSyntaxError('"agencycountryindicators" tag got an unknown variable: %r' % self.agency)

            try:
                country = self.country.resolve(context)
            except VariableDoesNotExist:
                raise TemplateSyntaxError('"agencycountryindicators" tag got an unknown variable: %r' % self.country)

            indicators = calc_agency_country_indicators(agency, country)
            for ind in ["2DPa", "4DP", "5DPa", "5DPb"]:
                (base_val, base_year, latest_val, latest_year), comments = indicators[ind]
                if not base_val in (None, NA_STR) and not latest_val in (None, NA_STR) and base_val != 0:
                    target_val = (latest_val - base_val) / base_val * 100
                    indicators[ind] = ((base_val, base_year, latest_val, latest_year, target_val), comments)

            (base_val, base_year, latest_val, latest_year), comments = indicators["5DPc"]
            if not base_val in (None, NA_STR) and not latest_val in (None, NA_STR) and base_val != 0:
                target_val = (1.0 - (latest_val / float(base_val)))  * 100
                indicators["5DPc"] = ((base_val, base_year, latest_val, latest_year, target_val), comments)
            
            context[self.out_var] = indicators
            return ""
        except:
            traceback.print_exc()


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

