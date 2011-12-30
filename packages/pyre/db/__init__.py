# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
This package contains the bases for building machinery that enable connections to database back
ends
"""


# templates: table rows with all fields set to None; used to update table entries
def template(table):
    """
    Build a row of {table} with all its fields set to {None}.
    """
    # build an instance, bypassing the constructor
    row = table.__new__(table)
    # iterate over the table fields
    for field in table.pyre_localFields:
        # set all attributes to {None}
        setattr(row, field.name, None)
    # and return the instance
    return row


# interfaces
from .DataStore import DataStore as datastore
# components
from .SQL import SQL as sql
from .Server import Server as server
# the table class
from .Table import Table as table
# the base query class
from .Query import Query as query
# the data model
from .. import schema
from .Field import Field as field


# the representation of NULL
null = object()
# the representation of DEFAULT
default = object()


# descriptor factories
from .fields import (
    Boolean as bool,
    Date as date,
    Decimal as decimal,
    Float as float,
    Integer as int,
    Reference as reference,
    String as str,
    Time as time,
    )

# cascade action markers for foreign keys
from .actions import noAction, restrict, cascade, setNull, setDefault

# orderings
from .Collation import Collation as collation

def ascending(field):
    """
    Build a clause for the {ORDER} expression that marks {field} as sorted in ascending order
    """
    return collation(field=field, collation="ASC")


def descending(field):
    """
    Build a clause for the {ORDER} expression that marks {field} as sorted in descending order
    """
    return collation(field=field, collation="DESC")


# end of file 
