#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that standard SQL refuses to create a table that declares an index, since the
language has no indexes
"""


def test():
    """
    Declare a table with an index, and check the standard mill refuses to create it
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        # the name
        name = pyre.db.str()
        # the start of the acquisition
        start = pyre.db.timestamp()
        # and its end
        stop = pyre.db.timestamp()
        # the track, when it is known
        track = pyre.db.int()

    # index the acquisitions by their time span
    Granule.pyre_index(Granule.start, Granule.stop)
    # and its exceptions
    from pyre.db import exceptions

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="indexes")
    # attempt to
    try:
        # build the statements that create the table
        statement = tuple(mill.createTable(table=Granule))
    # which must fail
    except exceptions.NotSupportedError as error:
        # naming the index
        assert "the index granules_start_stop_index" in str(error), str(error)
    # if it doesn't
    else:
        # the table was created without its index
        assert False, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
