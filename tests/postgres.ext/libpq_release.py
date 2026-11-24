#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a released statement is gone, and that its name is free to be used again
"""


def test():
    """
    Prepare a statement, release it, and prepare another under the same name
    """
    # access the bindings
    from pyre.extensions import libpq

    # and the exceptions the package raises
    from pyre.db import exceptions

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # teach it a statement
    connection.prepare("pyre_one", "SELECT 1")
    # and make it forget
    connection.release("pyre_one")
    # attempt to
    try:
        # run what it forgot
        connection.execPrepared("pyre_one")
    # which is refused, the way the server reports a missing prepared statement
    except exceptions.OperationalError as error:
        # with its own code for it
        assert error.sqlstate == "26000", error.sqlstate
    # anything else
    else:
        # is a failure
        assert False, "a released statement ran"

    # the name is free, so teach it another statement under it
    connection.prepare("pyre_one", "SELECT 2")
    # which is the one that runs
    ((two,),) = connection.execPrepared("pyre_one")
    # so say
    assert two == 2, two
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
