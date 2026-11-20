#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an argument with a zero octet in it is refused, rather than cut short
"""


def test():
    """
    Send a string that holds a zero octet as the argument of a statement
    """
    # access the bindings
    from pyre.extensions import libpq

    # and the exceptions the package raises
    from pyre.db import exceptions

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # carefully
    try:
        # send a string with a zero octet in the middle
        answer = connection.execute("SELECT $1::text AS echo", "before\x00after")
    # postgres text cannot hold one, so the statement must fail
    except exceptions.DataError:
        # which is what we expect
        return
    # if it ran, the server saw something other than what we sent
    assert False, f"the argument was accepted, and came back as {answer[0][0]!r}"


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
