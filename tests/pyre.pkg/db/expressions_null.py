#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a restriction to the rows whose field is {NULL} renders
"""


def test():
    """
    Render a query whose restriction is a test of {NULL}
    """
    # access the package
    import pyre.db

    # a table of streets
    class Street(pyre.db.table, id="streets"):
        """
        Street names
        """

        # the name
        name = pyre.db.str()

    # the streets without a name
    class Streets(pyre.db.query, street=Street):
        """
        The streets without a name
        """

        # the field
        name = street.name
        # the restriction
        where = pyre.db.isNull(street.name)

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="expressions_null")
    # generate the statement
    statement = tuple(mill.select(Streets))
    # the restriction is the last line
    assert statement[-1] == "    (street.name IS NULL);", statement[-1]
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
