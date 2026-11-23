# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Join import Join


# declaration
class LeftJoin(Join):
    """
    The join of {table} to the other tables of a query that keeps the rows of the others that
    have no match in it
    """

    # the words that introduce me in a selection
    keyword = "LEFT JOIN"


# end of file
