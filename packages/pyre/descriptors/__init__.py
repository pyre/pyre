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
bool = mix(schemata.bool, descriptor)
decimal = mix(schemata.decimal, descriptor)
float = mix(schemata.float, descriptor)
inet = mix(schemata.inet, descriptor)
int = mix(schemata.int, descriptor)
identity = mix(schemata.identity, descriptor)
str = mix(schemata.str, descriptor)

# next the more complex types
date = mix(schemata.date, descriptor)
dimensional = mix(schemata.dimensional, descriptor)
time = mix(schemata.time, descriptor)
uri = mix(schemata.uri, descriptor)


# end of file 
