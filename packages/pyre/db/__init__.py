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
# the representation of DEFAULT
default = object()


# descriptor factories
from .columns import (
    Boolean as bool,
    Date as date,
    Decimal as decimal,
    Float as float,
    Integer as int,
    String as str,
    Time as time,
    )


# end of file 
