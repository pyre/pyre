# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the mill that speaks standard SQL
from .Standard import Standard as standard

# and the dialects of the back ends
from .Postgres import Postgres as postgres
from .SQLite import SQLite as sqlite

# end of file
