# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# declaration
class Join:
    """
    The join of {table} to the other tables of a query, matching the rows that satisfy {on}
    """

    # the words that introduce me in a selection
    keyword = "JOIN"

    # meta-methods
    def __init__(self, table, on, **kwds):
        # chain up
        super().__init__(**kwds)
        # the table i join
        self.table = table
        # and the predicate its rows must satisfy
        self.on = on
        # all done
        return


# end of file
