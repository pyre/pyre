# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved
# (c) 1998-2025 all rights reserved


"""
This package provides access to the factories for typed properties
"""

# get the typed class
from .Property import Property as property

# for convenience, expose the typed ones
# the simple ones
bool = property.bool
complex = property.complex
decimal = property.decimal
enum = property.enum
float = property.float
inet = property.inet
int = property.int
identity = property.identity
object = property.identity
str = property.str

# the more complex types
date = property.date
dimensional = property.dimensional
path = property.path
time = property.time
timestamp = property.timestamp
uri = property.uri

# containers
# array needs a patch; see below
list = property.list
set = property.set
tuple = property.tuple

# meta
istream = property.istream
ostream = property.ostream
envvar = property.envvar
envpath = property.envpath

from .Facility import Facility as facility

# meta-properties: trait descriptors for homogeneous containers; these require other trait
# descriptors to specify the type of the contents
from .Dict import Dict as dict


# the decorators
from ..descriptors import converter, normalizer, validator


# patch array so it can get a workable default schema
class array(property.array):
    # metamethods
    def __init__(self, schema=float, **kwds):
        # chain up
        super().__init__(schema=schema, **kwds)
        # all done
        return


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


def kv(default=object, **kwds):
    """
    A (key, value) table of strings
    """
    # normalize the default
    default = {} if default is object else default
    # build a dictionary that maps strings to strings
    return dict(schema=str(), default=default, **kwds)


def catalog(default=object, schema=None, **kwds):
    """
    A {dict} of {list}s
    """
    # normalize the default
    default = {} if default is object else default
    # if the user didn't specify a schema
    if schema is None:
        # default to string
        schema = str()
    # build a dictionary that maps strings to lists
    return dict(schema=list(schema=schema, **kwds), default=default)


def choices(default=object, schema=None, **kwds):
    """
    A {dict} of {set}s
    """
    # normalize the default
    default = {} if default is object else default
    # if the user didn't specify a schema
    if schema is None:
        # default to string
        schema = str()
    # build a dictionary that map strings to sets
    return dict(schema=set(schema=schema, **kwds), default=default)


# end of file
