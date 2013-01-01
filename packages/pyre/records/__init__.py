# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# data records
from .Record import Record as record
from .DynamicRecord import DynamicRecord as dynamicrecord

from .Entry import Entry as entry
field = entry.variable
derivation = entry.operator


# persistence
from .CSV import CSV as csv


# convenience factories
# access to the type specifiers
from .. import schema

def float(default=0, **kwds):
    descriptor = field(**kwds)
    descriptor.schema = schema.float
    descriptor.default = default
    return descriptor


def int(default=0, **kwds):
    descriptor = field(**kwds)
    descriptor.schema = schema.int
    descriptor.default = default
    return descriptor


def str(default="", **kwds):
    descriptor = field(**kwds)
    descriptor.schema = schema.str
    descriptor.default = default
    return descriptor


# end of file 
