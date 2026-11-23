#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that standard SQL refuses a column of floating point numbers of a width it has no type for
"""


def test():
    """
    Declare a table with a column of 16 bit floating point numbers, and check the standard mill
    refuses it
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # a table of samples
    class Samples(pyre.db.table, id="samples"):
        # their values
        value = pyre.db.float(bits=16)

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="columns_float_refused")
    # attempt to
    try:
        # build the statement that creates the table
        statement = tuple(mill.createTable(table=Samples))
    # which must fail
    except exceptions.NotSupportedError as error:
        # naming the column
        assert error.column == "value", error.column
        # and the width
        assert "16 bit floating point numbers" in str(error), str(error)
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
