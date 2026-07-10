#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Open a session with the back end through the low level interface, and verify that a session that
has been closed stays closed, however many copies of it are still lying around
"""


def test():
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
    # over a socket, to a server that told us its version
    assert connection.socket >= 0
    assert connection.server > 0

    # take a copy; the two now share one session with the server
    alias = connection
    # which the copy can use
    assert alias.exec("SELECT 1")[0][0] == "1"

    # close the session through one of them
    connection.close()
    # the one that closed it knows
    assert not connection.ok
    # and so does the copy; this is the whole point of the rewrite, since the bindings this
    # package replaces would have handed libpq an address it had already freed
    assert not alias.ok

    # a statement sent through the copy is a mistake on this side of the wire
    try:
        alias.exec("SELECT 1")
        assert False, "a closed session ran a statement"
    except exceptions.InterfaceError:
        pass

    # closing a session twice is harmless
    connection.close()

    # a session that cannot be established raises, rather than handing back something unusable
    try:
        libpq.Connection({"dbname": "pyre-no-such-database"})
        assert False, "connected to a database that does not exist"
    except exceptions.OperationalError:
        pass

    # a password with a space in it must not corrupt the specification; the connection fails,
    # because the role does not exist, but it fails cleanly, as an operational error, rather
    # than by turning the password into a password and a garbage keyword
    try:
        libpq.Connection({"dbname": "postgres", "user": "pyre-no-such-role", "password": "a b c"})
        assert False, "connected as a role that does not exist"
    except exceptions.OperationalError:
        pass

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
