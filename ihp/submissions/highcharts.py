import random
from numbers import Real, Integral

def ffloat(x):
    if x == None: return "0"
    try:
        x = float(x)
        return "%.1f" % x
    except:
        return "0"

class ChartObject(object):
    def __init__(self, tabs=0):
        super(ChartObject, self).__init__()
        self._tabs = tabs 

    @property
    def padding(self):
        return "".join(["\t"] * self._tabs)

    def _format(self, v):
        if isinstance(v, basestring):
            if v == "false" or v == "true":
                return v
            elif v.startswith("function"):
                return v
            return "'%s'" % v
        elif type(v) == list or type(v) == tuple:
            return "[" + ",".join(self._format(i) for i in v) + "]"
        elif isinstance(v, Integral):
            return str(v)
        elif isinstance(v, Real):
            return ffloat(v)
        elif type(v) == dict:
            p = ChartObject(self._tabs + 1)
            p.__dict__.update(v)
            return str(p)
        elif type(v) == ChartObject:
            p = ChartObject()
            p.__dict__.update(v.__dict__)
            p.__dict__["_tabs"] = self._tabs + 1
            return str(p)
        else:
            return ffloat(0)
            import pdb; pdb.set_trace()

    def __str__(self):
        padding = self.padding
        separator = ",\n%s\t" % (padding)
        contents = separator.join(["%s : %s" % (k, self._format(v)) for (k, v) in self.__dict__.items() if not k.startswith("_")])

        return """{\n%(padding)s\t%(contents)s\n%(padding)s}""" %  locals()

class Chart(ChartObject):
    def __init__(self, target_element):
        super(Chart, self).__init__(tabs=1)
        self.var_name = "chart_%s" % (random.randint(0, 10000000))
        self._target_element = target_element

    def __str__(self):
        chart = self.__dict__.setdefault("chart", ChartObject())
        if type(chart) == dict:
            chart["renderTo"] = self._target_element
        else:
            chart.renderTo = self._target_element
        
        content = super(Chart, self).__str__().strip()
        var_name = self.var_name
        return """ 
var %(var_name)s; // globally available
$(document).ready(function() {
    %(var_name)s = new Highcharts.Chart(
    %(content)s);
});
""" % locals()
