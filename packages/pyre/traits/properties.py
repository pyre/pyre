# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
This package provides access to the factories for typed properties
"""

# get the typed class
from .Property import Property as property

# for convenience, expose the typed ones
# the simple ones: truth values
bool = property.bool
# strings of octets
bytes = property.bytes
# the types of the cells of grids
cell = property.cell
# complex numbers
complex = property.complex
# fixed point decimals
decimal = property.decimal
# one of a set of names
enum = property.enum
# floating point numbers
float = property.float
# internet addresses
inet = property.inet
# integers
int = property.int
# values taken as they are
identity = property.identity
# the same, by another name
object = property.identity
# strings
str = property.str

# the more complex types: dates
date = property.date
# quantities with units
dimensional = property.dimensional
# json documents
json = property.json
# filesystem paths
path = property.path
# times of day
time = property.time
# points in time
timestamp = property.timestamp
# resource identifiers
uri = property.uri
# universally unique identifiers
uuid = property.uuid

# containers: arrays
array = property.array
# lists
list = property.list
# sets
set = property.set
# tuples
tuple = property.tuple

# meta: input streams
istream = property.istream
# output streams
ostream = property.ostream
# environment variables
envvar = property.envvar
# search paths in the environment
envpath = property.envpath
# channels between processes
channel = property.channel

# the trait that holds a component
from .Facility import Facility as facility

# meta-properties: trait descriptors for homogeneous containers; these require other trait
# descriptors to specify the type of the contents
from .Dict import Dict as dict

# the decorators
from ..descriptors import converter, normalizer, validator


# common meta-descriptors
def strings(**kwds):
    """
    A list of strings
    """
    # build a descriptor that describes a list of strings
    return list(schema=str(), **kwds)


def paths(**kwds):
    """
    A list of paths
    """
    # build a descriptor that describes a list of paths and return it
    return list(schema=path(), **kwds)


def uris(**kwds):
    """
    A list of URIs
    """
    # build a descriptor that describes a list of uris and return it
    return list(schema=uri(), **kwds)


def kv(**kwds):
    """
    A (key, value) table of strings
    """
    # build a dictionary that maps strings to strings
    return dict(schema=str(), **kwds)


def catalog(schema=None, **kwds):
    """
    A {dict} of {list}s
    """
    # if the user didn't specify a schema
    if schema is None:
        # default to string
        schema = str()
    # build a dictionary that maps strings to lists
    return dict(schema=list(schema=schema), **kwds)


def choices(schema=None, **kwds):
    """
    A {dict} of {set}s
    """
    # if the user didn't specify a schema
    if schema is None:
        # default to string
        schema = str()
    # build a dictionary that map strings to sets
    return dict(schema=set(schema=schema), **kwds)


# end of file
