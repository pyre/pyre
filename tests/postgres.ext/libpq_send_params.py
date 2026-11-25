#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a statement can be sent with the values of its placeholders without waiting for the
server, with the values rendered as those of {execute}
"""


def test():
    """
    Send a statement with its arguments without waiting, and collect its answer
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # send a statement with two arguments, without waiting
    connection.sendParams("SELECT $1::integer * 2, upper($2::text)", 21, "pyre")
    # its answer holds the row
    answer = connection.result()
    # with both values worked out by the server
    assert tuple(answer[0]) == (42, "PYRE"), tuple(answer[0])
    # and nothing follows it
    assert connection.result() is None
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
