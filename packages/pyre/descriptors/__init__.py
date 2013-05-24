# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# the descriptor base class and its functionals
from .Descriptor import Descriptor as stem, descriptor, operator, literal

# decorators for value processors
from .Converter import Converter as converter
from .Normalizer import Normalizer as normalizer
from .Validator import Validator as validator


# a class generator that will build a typed descriptor from a base of your choice
def mix(schema, descriptor=descriptor):
    """
    Build a typed descriptor by subclassing {descriptor} and {schema}
    """
    # easy enough
    return type(schema.typename, (descriptor, schema), {})


# get the schemata
from .. import schemata

# build the typed descriptors; first the simple ones
class bool(descriptor, schemata.bool): pass
class decimal(descriptor, schemata.decimal): pass
class float(descriptor, schemata.float): pass
class inet(descriptor, schemata.inet): pass
class int(descriptor, schemata.int): pass
class identity(descriptor, schemata.identity): pass
class str(descriptor, schemata.str): pass

# next, the more complex types
class date(descriptor, schemata.date): pass
class dimensional(descriptor, schemata.dimensional): pass
class time(descriptor, schemata.time): pass
class uri(descriptor, schemata.uri): pass

# finally, containers
class list(descriptor, schemata.list): pass
class set(descriptor, schemata.set): pass
class tuple(descriptor, schemata.tuple): pass


# end of file 
