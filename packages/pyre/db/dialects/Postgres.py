# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my superclass
from .Standard import Standard


# declaration
class Postgres(Standard, family="pyre.db.dialects.postgres"):
    """
    Generate SQL statements in the dialect of postgres: standard SQL, except where postgres spells
    things differently
    """


# end of file
