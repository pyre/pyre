# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my superclass
from .Standard import Standard

# the type declarators of my columns
from .PostgresColumns import PostgresColumns

# and the literals of their values
from .PostgresLiterals import PostgresLiterals


# declaration
class Postgres(Standard, family="pyre.db.dialects.postgres"):
    """
    Generate SQL statements in the dialect of postgres: standard SQL, except where postgres departs
    from it
    """

    # the visitor that builds the type declarators of my columns
    columns = PostgresColumns
    # and the one that renders the literals of their values
    literals = PostgresLiterals


# end of file
