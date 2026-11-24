#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a statement can be prepared and run without waiting for the server, with the values
of its placeholders rendered as those of {execute}
"""


def test():
    """
    Prepare a statement and run it without waiting, collecting each answer
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # teach the server a statement, without waiting
    connection.sendPrepare("pyre_send_prepared", "SELECT $1::integer * 2")
    # its answer says it was taught
    assert connection.result().ok
    # and nothing follows it
    assert connection.result() is None
    # run it, without waiting
    connection.sendPrepared("pyre_send_prepared", 21)
    # its answer holds the row
    assert connection.result()[0][0] == 42
    # and nothing follows it
    assert connection.result() is None
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
