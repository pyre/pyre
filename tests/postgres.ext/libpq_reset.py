#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a session the server has ended can be brought back with the parameters it was opened
with
"""


def test():
    """
    End a session from another one, see it fail, reset it, and use it again
    """
    # access the package
    import pyre.db

    # and the bindings
    from pyre.extensions import libpq

    # open the session to end
    connection = libpq.Connection({"dbname": "postgres"})
    # note the process that serves it
    backend = connection.backend
    # open another
    other = libpq.Connection({"dbname": "postgres"})
    # and end the first one from it
    other.exec(f"SELECT pg_terminate_backend({backend})")

    # carefully
    try:
        # use the ended session
        connection.exec("SELECT 1")
    # the failure
    except pyre.db.exceptions.OperationalError:
        # is what a session the server has ended reports
        pass
    # a statement that runs
    else:
        # means the session was never ended
        assert False, "a session the server ended ran a statement"

    # bring the session back
    connection.reset()
    # it is up
    assert connection.ok
    # served by another process
    assert connection.backend != backend, connection.backend
    # and usable
    assert connection.exec("SELECT 1")[0][0] == 1
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
