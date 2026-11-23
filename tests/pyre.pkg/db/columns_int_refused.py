#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that standard SQL refuses a column of integers of a width it has no type for
"""


def test():
    """
    Declare a table with a column of 48 bit integers, and check the standard mill refuses it
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # a table of granules
    class Granules(pyre.db.table, id="granules"):
        # their sizes
        size = pyre.db.int(bits=48)

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="columns_int_refused")
    # attempt to
    try:
        # build the statement that creates the table
        statement = tuple(mill.createTable(table=Granules))
    # which must fail
    except exceptions.NotSupportedError as error:
        # naming the column
        assert error.column == "size", error.column
        # and the width
        assert "48 bit integers" in str(error), str(error)
    # if it doesn't
    else:
        # the column was declared anyway
        assert False, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
