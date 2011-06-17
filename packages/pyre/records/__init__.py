# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# data records
from .Record import Record as record
from .DynamicRecord import DynamicRecord as dynamicrecord

from .Field import Field as field
from .Derivation import Derivation as derivation


# persistence
from .CSV import CSV as csv


# convenience factories
# access to the type specifiers
import pyre.schema

def float(default=0, **kwds):
    descriptor = field(**kwds)
    descriptor.type = pyre.schema.float
    descriptor.default = default
    return descriptor


def int(default=0, **kwds):
    descriptor = field(**kwds)
    descriptor.type = pyre.schema.int
    descriptor.default = default
    return descriptor


def str(default="", **kwds):
    descriptor = field(**kwds)
    descriptor.type = pyre.schema.str
    descriptor.default = default
    return descriptor


# end of file 
