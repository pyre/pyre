#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Open a session with the back end through the low level interface, and verify that a session
    that has been closed stays closed, however many copies of it are still lying around
    """
    # access the bindings
    from pyre.extensions import libpq

    # and the exceptions the package raises, which are the very ones {pyre.db} publishes
    from pyre.db import exceptions

    # open a session; each parameter is a name and a value, kept apart all the way down
    connection = libpq.Connection({"dbname": "postgres"})
    # it should be up
    assert connection.ok
    # and talking to the database we asked for
    assert connection.database == "postgres"
    # over a socket
    assert connection.socket >= 0
    # to a server that told us its version
    assert connection.server > 0

    # take a copy; the two now share one session with the server
    alias = connection
    # which the copy can use
    assert alias.exec("SELECT 1")[0][0] == 1

    # close the session through one of them
    connection.close()
    # the one that closed it knows
    assert not connection.ok
    # and so does the copy, so nothing hands libpq a session it has already freed
    assert not alias.ok

    # a statement sent through the copy is a mistake on this side of the wire
    try:
        # send one
        alias.exec("SELECT 1")
        # and complain if it ran
        assert False, "a closed session ran a statement"
    # the refusal
    except exceptions.InterfaceError:
        # is what should happen, so there is nothing else to check
        pass

    # closing a session twice is harmless
    connection.close()

    # a session that cannot be established raises, rather than handing back something unusable
    try:
        # ask for a database that is not there
        libpq.Connection({"dbname": "pyre-no-such-database"})
        # and complain if the session opened
        assert False, "connected to a database that does not exist"
    # the refusal
    except exceptions.OperationalError:
        # is what should happen, so there is nothing else to check
        pass

    # a password with a space in it must not corrupt the specification; the connection fails,
    # because the role does not exist, but it fails cleanly, as an operational error, rather
    # than by turning the password into a password and a garbage keyword
    try:
        # ask for a role that is not there
        libpq.Connection({"dbname": "postgres", "user": "pyre-no-such-role", "password": "a b c"})
        # and complain if the session opened
        assert False, "connected as a role that does not exist"
    # the refusal
    except exceptions.OperationalError:
        # is what should happen, so there is nothing else to check
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
