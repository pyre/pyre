#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a negative subscript counts the columns of a row back from its end, as it does for a
python sequence
"""


def test():
    """
    Read the columns of a row from its end, and step past its start
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # select a row of three columns
    row = connection.exec("SELECT 1, 2, 3")[0]
    # the last column
    assert row[-1] == 3, row[-1]
    # and the first, counted from the end
    assert row[-3] == 1, row[-3]
    # carefully
    try:
        # step past the start
        row[-4]
    # the failure
    except IndexError:
        # is the one python expects
        pass
    # a value
    else:
        # means the subscript wrapped around
        assert False, "a subscript past the start of the row found a column"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
