#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a cast declared in a query is one of its projections
"""


def test():
    """
    Render a query that selects the number of a house as text
    """
    # access the package
    import pyre.db

    # a table of houses
    class House(pyre.db.table, id="houses"):
        """
        Houses, by number
        """

        # the number
        number = pyre.db.int()

    # the numbers of the houses, as text
    class Labels(pyre.db.query, house=House):
        """
        The numbers of the houses, as text
        """

        # the label
        label = pyre.db.cast(house.number, pyre.db.str())

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="expressions_cast_projection")
    # generate the statement
    statement = tuple(mill.select(Labels))
    # and check it
    assert statement == (
        "SELECT",
        "    CAST(house.number AS CLOB) AS label",
        "  FROM",
        "    houses AS house;",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
