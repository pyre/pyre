# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Machinery for building connections to database back ends
"""

# the literals
from .literals import null, default

# cascade action markers for foreign keys
from .actions import noAction, restrict, cascade, setNull, setDefault

# orderings
from .Collation import Collation as collation


# for convenience
def ascending(fieldref):
    """
    Build a clause for the {ORDER} expression that marks {fieldref} as sorted in ascending
    order
    """
    # build and return a collation object
    return collation(fieldref=fieldref, collation="ASC")


def descending(fieldref):
    """
    Build a clause for the {ORDER} expression that marks {fieldref} as sorted in descending
    order
    """
    # build and return a collation object
    return collation(fieldref=fieldref, collation="DESC")


# primitive SQL expressions
from .expressions import (
    IsNull as isNull,
    IsNotNull as isNotNull,
    Cast as cast,
    Like as like,
)

# field declarations
from ..records import field

# the local measure class
from .Measure import Measure as measure

# the typed measures, one for each type a column can hold
array = measure.array  # arrays of the values of another column type
bool = measure.bool  # truth values
bytes = measure.bytes  # strings of octets
date = measure.date  # dates
decimal = measure.decimal  # fixed point numbers
float = measure.float  # floating point numbers
int = measure.int  # integers
str = measure.str  # text
time = measure.time  # times of day
timestamp = measure.timestamp  # moments in time
uuid = measure.uuid  # universally unique identifiers
# references to external keys
from .Reference import Reference as reference

# tables
from .Table import Table as table

# queries
from .Query import Query as query

# persistent object
from .Object import Object as object

# protocols
from .DataStore import DataStore as datastore

# components
from .dialects import standard as sql
from .Server import Server as server
from .Client import Client as client

# supported servers
from .Backup import Backup as backup
from .SQLite import SQLite as sqlite
from .Postgres import Postgres as postgres


# templates: table rows with all fields set to None; used to update table entries
def template(table):
    """
    Build a row of {table} with all its fields set to {None}.
    """
    # build an instance, bypassing the constructor
    row = table.pyre_mutable(data=(None,) * len(table.pyre_fields))
    # and return it
    return row


# end of file
