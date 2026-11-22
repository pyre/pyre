# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Machinery for building connections to database back ends
"""

# the literals
from .schema import null, default

# cascade action markers for foreign keys
from .schema import noAction, restrict, cascade, setNull, setDefault

# orderings
from .queries import collation


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
from .queries import isNull, isNotNull, cast, like

# field declarations
from ..records import field

# the local measure class
from .schema import measure

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
from .schema import reference

# tables
from .schema import table

# queries
from .queries import query

# persistent object
from .objects import object

# protocols
from .DataStore import DataStore as datastore

# components: the base of the servers, which brings in the mill of standard SQL
from .Server import Server as server
from .Client import Client as client

# the back ends
from . import backends

# the mill that speaks standard SQL
from .backends.standard import mill as sql

# supported servers
from .Backup import Backup as backup
from .backends.sqlite import server as sqlite
from .backends.postgres import server as postgres


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
