# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my superclass
from ..standard import Mill as standard

# the type declarators of my columns
from .Columns import Columns

# and the literals of their values
from .Literals import Literals


# declaration
class Mill(standard.Mill, family="pyre.db.dialects.sqlite"):
    """
    Generate SQL statements in the dialect of sqlite: standard SQL, except where sqlite departs
    from it
    """

    # the name of my language, for the explanations of refusals
    dialect = "sqlite"

    # the visitor that builds the type declarators of my columns
    columns = Columns
    # and the one that renders the literals of their values
    literals = Literals


# end of file
