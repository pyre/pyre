# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


# access to the basic objects in the package
from .Sheet import Sheet as sheet

from .Record import Record as record
from .Measure import Measure as measure
from .Derivation import Derivation as derivation

# readers/writers
from .CSV import CSV as csv


# access the type declarators
from .. import schema


# measure factories with type information
def dimensional(default=0):
    """
    Build a measure that has units; legal assignments are constrained to have units that match
    those of the default value supplied
    """
    m = measure()
    m.type = schema.dimensional
    m.default = default
    return m


def float(default=0):
    """
    Build a float measure
    """
    m = measure()
    m.type = schema.float
    m.default = default
    return m


def int(default=0):
    """
    Build an integer measure
    """
    m = measure()
    m.type = schema.int
    m.default = default
    return m


def str(default=""):
    """
    Build a string measure
    """
    m = measure()
    m.type = schema.str
    m.default = default
    return m


# end of file 
