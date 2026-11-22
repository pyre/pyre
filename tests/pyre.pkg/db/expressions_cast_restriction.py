#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a cast takes part in a comparison
"""


def test():
    """
    Render a query whose restriction compares a cast to a number
    """
    # access the package
    import pyre.db

    # a table of things, known by codes that are text
    class Thing(pyre.db.table, id="things"):
        """
        Things, by code
        """

        # the code
        code = pyre.db.str(maxlen=8)

    # the numbers of the things whose code is greater than three
    class Numbers(pyre.db.query, thing=Thing):
        """
        The codes of the things, as numbers
        """

        # the number
        number = pyre.db.cast(thing.code, pyre.db.int())
        # the restriction
        where = pyre.db.cast(thing.code, pyre.db.int()) > 3

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="expressions_cast_restriction")
    # generate the statement
    statement = tuple(mill.select(Numbers))
    # the restriction is the last line
    assert statement[-1] == "    ((CAST(thing.code AS INTEGER)) > (3));", statement[-1]
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
