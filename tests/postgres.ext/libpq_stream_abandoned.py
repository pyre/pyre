#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a stream abandoned before its last row leaves the session usable
"""


def test():
    """
    Read the first batch of a long stream, abandon the rest, and use the session
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # go through the batches of many rows
    for batch in connection.stream("SELECT generate_series(1, 1000000)", batch=100):
        # but stop after the first
        break
    # the session is free
    assert connection.transaction == libpq.TransactionStatus.idle
    # and usable
    assert connection.exec("SELECT 1")[0][0] == 1
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
