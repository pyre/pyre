#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a stream whose statement fails partway hands back the rows made before the failure,
and raises the exception of the condition the server named
"""


def test():
    """
    Stream a selection that divides by zero at its third row
    """
    # access the package
    import pyre.db

    # and the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # the values of the rows that arrive
    values = []
    # carefully
    try:
        # go through the batches, one row at a time
        for batch in connection.stream(
            "SELECT 10 / (3 - n) FROM generate_series(1, 5) AS n", batch=1
        ):
            # and keep the values of their rows
            values.extend(row[0] for row in batch)
    # the failure
    except pyre.db.exceptions.DataError as error:
        # is the division by zero
        assert error.sqlstate == "22012", error.sqlstate
    # reading to the end
    else:
        # means the failure was lost
        assert False, "the stream ended without a word"
    # the rows before the failure arrived
    assert values == [5, 10], values
    # and the session is usable
    assert connection.exec("SELECT 1")[0][0] == 1
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
