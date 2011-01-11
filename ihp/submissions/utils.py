import inspect, types, __builtin__

############## preliminary: two utility functions #####################

def skip_redundant(iterable, skipset=None):
    "Redundant items are repeated items or items in the original skipset."
    if skipset is None: skipset = set()
    for item in iterable:
        if item not in skipset:
            skipset.add(item)
            yield item


def remove_redundant(metaclasses):
    skipset = set([types.ClassType])
    for meta in metaclasses: # determines the metaclasses to be skipped
        skipset.update(inspect.getmro(meta)[1:])
    return tuple(skip_redundant(metaclasses, skipset))

##################################################################
## now the core of the module: two mutually recursive functions ##
##################################################################

memoized_metaclasses_map = {}

def get_noconflict_metaclass(bases, left_metas, right_metas):
    """Not intended to be used outside of this module, unless you know
    what you are doing."""
    # make tuple of needed metaclasses in specified priority order
    metas = left_metas + tuple(map(type, bases)) + right_metas
    needed_metas = remove_redundant(metas)

    # return existing confict-solving meta, if any
    if needed_metas in memoized_metaclasses_map:
      return memoized_metaclasses_map[needed_metas]
    # nope: compute, memoize and return needed conflict-solving meta
    elif not needed_metas:         # wee, a trivial case, happy us
        meta = type
    elif len(needed_metas) == 1: # another trivial case
       meta = needed_metas[0]
    # check for recursion, can happen i.e. for Zope ExtensionClasses
    elif needed_metas == bases: 
        raise TypeError("Incompatible root metatypes", needed_metas)
    else: # gotta work ...
        metaname = '_' + ''.join([m.__name__ for m in needed_metas])
        meta = classmaker()(metaname, needed_metas, {})
    memoized_metaclasses_map[needed_metas] = meta
    return meta

def classmaker(left_metas=(), right_metas=()):
    def make_class(name, bases, adict):
        metaclass = get_noconflict_metaclass(bases, left_metas, right_metas)
        return metaclass(name, bases, adict)
    return make_class

# A float class that allows for safe arithmetic operations with nones
class none_num(float):

    def __new__(cls, value):
        if value == None:
            value = 0
        try:
            float(value)
            return float.__new__(cls, value)
        except:
            return value

    def _either_none(self, other):
        return self.ovalue == None or other == None

    def __init__(self, value):
        self.ovalue = value

    def __add__(self, other):
        if self._either_none(other): return none_num(None)
        return none_num(super(none_num, self).__add__(other))

    def __div__(self, other):
        if self._either_none(other): return none_num(None)
        if other == 0: return none_num(None)
        return none_num(super(none_num, self).__div__(other))

    def __mul__(self, other):
        if self._either_none(other): return none_num(None)
        return none_num(super(none_num, self).__mul__(other))

    def __sub__(self, other):
        if self._either_none(other): return none_num(None)
        return none_num(super(none_num, self).__sub__(other))

    def __neg__(self):
        if self.ovalue == None: return none_num(None)
        else:
            return none_num(super(none_num, self).__neg__())

    def __rsub__(self, other):
        return -self.__sub__(other)

    def __eq__(self, other):
        return self.ovalue == other

