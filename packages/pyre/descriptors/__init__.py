# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# the descriptor base class
from .Descriptor import Descriptor as stem

# decorators for value processors
from .Converter import Converter as converter
from .Normalizer import Normalizer as normalizer
from .Validator import Validator as validator


# get the schemata
from .. import schemata

# build the typed descriptors
@schemata.typed
class descriptor(stem.variable): pass

# for convenience, expose the typed ones
# first the simple ones
bool = descriptor.bool
decimal = descriptor.decimal
float = descriptor.float
inet = descriptor.inet
int = descriptor.int
identity = descriptor.identity
str = descriptor.str

# next, the more complex types
date = descriptor.date
dimensional = descriptor.dimensional
time = descriptor.time
uri = descriptor.uri

# finally, containers
array = descriptor.array
list = descriptor.list
set = descriptor.set
tuple = descriptor.tuple


# end of file 
