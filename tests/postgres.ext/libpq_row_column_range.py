#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a subscript of a row past its columns raises an IndexError that names a column, and
that a negative subscript counts back from the last column
"""


def test():
    """
    Read a row of two columns past its end, and from its end
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # get a row of two columns
    row = connection.exec("SELECT 1, 2")[0]
    # a negative subscript counts back from the last column
    assert row[-1] == 2
    # carefully
    try:
        # read past the end
        row[5]
    # the failure
    except IndexError as error:
        # names a column
        assert "column" in str(error), str(error)
    # reading past the end
    else:
        # is a failure that was lost
        assert False, "a row handed back a column it does not have"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
