#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a statement sent through a session in the middle of a stream is refused as a misuse of
the interface, and that the stream hands back the rest of its rows
"""


def test():
    """
    Start a stream, send another statement, and read the rest of the stream
    """
    # access the package
    import pyre.db

    # and the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # stream five rows, two at a time
    stream = connection.stream("SELECT generate_series(1, 5)", batch=2)
    # take the first batch
    rows = len(next(stream))
    # carefully
    try:
        # send another statement in the middle of the stream
        connection.exec("SELECT 42")
    # the refusal
    except pyre.db.exceptions.InterfaceError:
        # is what is expected
        refused = True
    # a statement that ran
    else:
        # means the stream was thrown away
        refused = False
    # make sure the statement was refused
    assert refused
    # the stream hands back the rest of its rows
    rows += sum(len(batch) for batch in stream)
    # all of them
    assert rows == 5, rows
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
