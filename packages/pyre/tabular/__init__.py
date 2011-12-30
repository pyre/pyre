# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# access to the basic objects in the package
from .Sheet import Sheet as sheet # basic data tables
from .Chart import Chart as chart # coördinate systems
from .Pivot import Pivot as pivot # pivot tables
# column descriptors
from .Measure import Measure as measure
# readers/writers
from .CSV import CSV as csv


# access the type declarators
from .. import schema


# convenience factories that build measures of specific types
def dimensional(default=0, **kwds):
    """
    Build a measure that has units

    Legal assignments are constrained to have units compatible with the default value
    """
    m = measure(**kwds)
    m.type = schema.dimensional
    m.default = default
    return m


def float(default=0, **kwds):
    """
    Build a float measure
    """
    m = measure(**kwds)
    m.type = schema.float
    m.default = default
    return m


def int(default=0, **kwds):
    """
    Build an integer measure
    """
    m = measure(**kwds)
    m.type = schema.int
    m.default = default
    return m


def str(default="", **kwds):
    """
    Build a string measure
    """
    m = measure(**kwds)
    m.type = schema.str
    m.default = default
    return m


# dimension factories
from .InferredDimension import InferredDimension as inferred
from .IntervalDimension import IntervalDimension as interval


# end of file 
