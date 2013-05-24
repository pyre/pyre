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
# build the typed descriptors
# first the simple ones
bool = mix(schema=schemata.bool, descriptor=descriptor)
decimal = mix(schema=schemata.decimal, descriptor=descriptor)
float = mix(schema=schemata.float, descriptor=descriptor)
inet = mix(schema=schemata.inet, descriptor=descriptor)
int = mix(schema=schemata.int, descriptor=descriptor)
identity = mix(schema=schemata.identity, descriptor=descriptor)
str = mix(schema=schemata.str, descriptor=descriptor)

# next the more complex types
date = mix(schema=schemata.date, descriptor=descriptor)
dimensional = mix(schema=schemata.dimensional, descriptor=descriptor)
time = mix(schema=schemata.time, descriptor=descriptor)
uri = mix(schema=schemata.uri, descriptor=descriptor)

# finally, containers
list = mix(schema=schemata.list, descriptor=descriptor)
set = mix(schema=schemata.set, descriptor=descriptor)
tuple = mix(schema=schemata.tuple, descriptor=descriptor)


# end of file 
