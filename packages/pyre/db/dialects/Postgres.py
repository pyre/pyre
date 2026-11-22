# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my superclass
from .Standard import Standard

# the type declarators of my columns
from .PostgresColumns import PostgresColumns


# declaration
class Postgres(Standard, family="pyre.db.dialects.postgres"):
    """
    Generate SQL statements in the dialect of postgres: standard SQL, except where postgres departs
    from it
    """

    # the visitor that builds the type declarators of my columns
    columns = PostgresColumns


# end of file
