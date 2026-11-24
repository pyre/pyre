#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a stream fills the placeholders of its statement from its arguments, rendered as those
of {execute}
"""


def test():
    """
    Stream a series whose bounds travel beside the statement
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # stream the series
    stream = connection.stream("SELECT generate_series($1::integer, $2::integer)", 3, 7)
    # its rows are the ones the arguments asked for
    assert [row[0] for batch in stream for row in batch] == [3, 4, 5, 6, 7]
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
