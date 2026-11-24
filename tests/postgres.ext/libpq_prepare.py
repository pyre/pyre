#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a prepared statement runs as often as it is asked, each time with its own arguments
"""


def test():
    """
    Prepare a sum of two numbers, and run it twice
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # teach it a sum of two numbers
    connection.prepare("pyre_sum", "SELECT $1::int8 + $2::int4")
    # run it
    ((first,),) = connection.execPrepared("pyre_sum", 40, 2)
    # check the answer
    assert first == 42, first
    # run it again, with other arguments
    ((second,),) = connection.execPrepared("pyre_sum", 1, 2)
    # and check that it used them
    assert second == 3, second
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
