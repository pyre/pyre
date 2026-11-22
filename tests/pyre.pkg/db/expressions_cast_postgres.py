#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a cast renders the declarator of its target type in the dialect of postgres
"""


def test():
    """
    Render a cast of the number of a house to text
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

    # the number of a house, as text
    label = pyre.db.cast(House.number, pyre.db.str())

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.dialects.postgres(name="expressions_cast_postgres")
    # render the cast in the context of its table
    expression = mill.expression(root=label, context=House)
    # it names the type of its target as the dialect of postgres declares it
    assert expression == "CAST(number AS TEXT)", expression
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
