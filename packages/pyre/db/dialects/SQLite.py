# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my superclass
from .Standard import Standard

# the spellings of the types of my columns
from .SQLiteColumns import SQLiteColumns


# declaration
class SQLite(Standard, family="pyre.db.dialects.sqlite"):
    """
    Generate SQL statements in the dialect of sqlite: standard SQL, except where sqlite spells
    things differently
    """

    # the visitor that spells the types of my columns
    columns = SQLiteColumns


# end of file
