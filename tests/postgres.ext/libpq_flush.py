#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a session that sends without waiting leaves what the socket cannot take queued, and
that flushing pushes it out
"""


def test():
    """
    Send a statement too large for the socket without waiting, flush it out, and collect its
    answer
    """
    # externals
    import select
    import time

    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # make the calls that send return without waiting for the socket to drain
    connection.nonblocking(True)
    # a value far larger than a socket holds
    value = "x" * (16 * 1024 * 1024)
    # send a statement that carries it
    connection.sendParams("SELECT length($1::text)", value)

    # some of it is still queued
    assert connection.flush() == 1, "the whole statement went out at once"
    # give the rest a minute at most
    deadline = time.monotonic() + 60
    # until it has all gone
    while connection.flush() == 1:
        # wait for the socket to take more
        select.select([connection.socket], [connection.socket], [], 1)
        # and read whatever the server has sent, so it never waits on us
        connection.consume()
        # but not forever
        assert time.monotonic() < deadline, "the statement never went out"

    # the answer holds the length of the value
    assert connection.result()[0][0] == len(value)
    # and nothing follows it
    assert connection.result() is None
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
