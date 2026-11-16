# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


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
class descriptor(stem.variable):
    """
    The descriptor that carries a subclass for each of the schemata
    """


# for convenience, expose the typed ones
# the simple ones: truth values
bool = descriptor.bool
# complex numbers
complex = descriptor.complex
# fixed point decimals
decimal = descriptor.decimal
# one of a set of names
enum = descriptor.enum
# floating point numbers
float = descriptor.float
# internet addresses
inet = descriptor.inet
# integers
int = descriptor.int
# values taken as they are
identity = descriptor.identity
# strings
str = descriptor.str

# more complex types: dates
date = descriptor.date
# quantities with units
dimensional = descriptor.dimensional
# filesystem paths
path = descriptor.path
# times of day
time = descriptor.time
# points in time
timestamp = descriptor.timestamp
# resource identifiers
uri = descriptor.uri

# containers: arrays
array = descriptor.array
# lists
list = descriptor.list
# sets
set = descriptor.set
# tuples
tuple = descriptor.tuple

# meta-types: input streams
istream = descriptor.istream
# output streams
ostream = descriptor.ostream
# channels between processes
channel = descriptor.channel


# common meta-descriptors
def strings(default=list, **kwds):
    """
    A list of strings
    """
    # build a descriptor that describes a list of strings
    return list(schema=str(), default=default)


def uris(default=list, **kwds):
    """
    A list of URIs
    """
    # build a descriptor that describes a list of uris and return it
    return list(schema=uri(), default=default)


# end of file
