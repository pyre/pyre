# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
This package contains the bases for building machinery that enable connections to database back
ends
"""


# interfaces
from .DataStore import DataStore as datastore
# components
from .SQL import SQL as sql
from .Server import Server as server
# the table class
from .Table import Table as table
# the data model
from .. import schema
from .Column import Column as column


# the representation of NULL
null = object()

# descriptor factories
def bool(**kwds):
    """
    Booleans
    """
    c = column(**kwds)
    return c


def date(**kwds):
    """
    Support for dates
    """
    c = column(**kwds)
    return c


def decimal(precision=None, scale=None, **kwds):
    """
    Support for arbitrary precision numbers
    """
    c = column(**kwds)
    return c


def float(**kwds):
    """
    Double precision floating point numbers
    """
    c = column(**kwds)
    return c


def int(**kwds):
    """
    Integers
    """
    c = column(**kwds)
    c.type = schema.int
    return c


def str(maxlen=None, **kwds):
    """
    String of arbitrary length
    """
    c = column(**kwds)
    return c


def time(timezone=False, **kwds):
    """
    Time of day, with or without timezone
    """
    c = column(**kwds)
    return c


def timedelta(**kwds):
    """
    Time intervals with microsecond resolution
    """
    c = column(**kwds)
    return c


def timestamp(timezone=False, **kwds):
    """
    Both date and time of day, with or without timezone
    """
    c = column(**kwds)
    return c


# end of file 
