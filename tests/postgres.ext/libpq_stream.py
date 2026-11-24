#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a stream hands back the rows of a selection in batches, each one a result whose rows
are converted as those of {execute}
"""


def test():
    """
    Stream five rows two at a time, and check the batches and their rows
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # stream five rows, two at a time
    batches = list(connection.stream("SELECT generate_series(1, 5)", batch=2))
    # every batch is a result that holds at most two rows
    assert all(len(batch) <= 2 for batch in batches), batches
    # and together they hold every row, in order, as numbers
    assert [row[0] for batch in batches for row in batch] == [1, 2, 3, 4, 5], batches
    # the session is free
    assert connection.transaction == libpq.TransactionStatus.idle
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
