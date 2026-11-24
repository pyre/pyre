#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a copy whose block raises keeps none of its rows, lets the exception through, and
leaves the session usable
"""


# an exception of our own, so nothing else can be mistaken for it
class Interrupted(Exception):
    """
    Exception raised when the block of the copy gives up
    """


def test():
    """
    Raise inside the block of a copy, and check that the table is empty
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # make a table of our own, which goes away with the session
    connection.exec("CREATE TEMPORARY TABLE pyre_copy (id integer)")

    # whether the exception of the block got through
    through = False
    # attempt to
    try:
        # copy into it
        with connection.copyIn("COPY pyre_copy FROM STDIN") as copy:
            # a row
            copy.row(1)
            # and give up
            raise Interrupted()
    # the exception
    except Interrupted:
        # gets through
        through = True
    # as it should
    assert through, "the exception of the block was swallowed"

    # the table is empty
    ((count,),) = connection.exec("SELECT count(*) FROM pyre_copy")
    # so say
    assert count == 0, count
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
