#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a copy sent as an ordinary statement is refused as a misuse of the interface, and that
the session is usable afterwards
"""


def test():
    """
    Send a copy through {exec}, and check the refusal
    """
    # access the bindings
    from pyre.extensions import libpq

    # and the exceptions the package raises
    from pyre.db import exceptions

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # make a table of our own, which goes away with the session
    connection.exec("CREATE TEMPORARY TABLE pyre_copy (id integer)")
    # attempt to
    try:
        # send a copy as an ordinary statement
        connection.exec("COPY pyre_copy FROM STDIN")
    # which is refused
    except exceptions.InterfaceError as error:
        # naming the statement
        assert error.command == "COPY pyre_copy FROM STDIN", error.command
    # anything else
    else:
        # is a failure
        assert False, "a copy sent as an ordinary statement was accepted"

    # the session is usable
    ((one,),) = connection.exec("SELECT 1")
    # so say
    assert one == 1, one
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
