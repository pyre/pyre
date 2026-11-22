# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The description of what a query selects, and how
"""

# orderings
from .Collation import Collation as collation

# primitive SQL expressions
from .expressions import (
    IsNull as isNull,
    IsNotNull as isNotNull,
    Cast as cast,
    Like as like,
)

# queries
from .Query import Query as query

# end of file
