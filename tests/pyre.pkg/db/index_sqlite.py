#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the statement sqlite builds for an index
"""


def test():
    """
    Declare an index, and check the statement the dialect of sqlite builds for it
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
    # make a mill
    mill = pyre.db.backends.sqlite.mill(name="indexes")
    # build the statement
    statement = tuple(mill.createIndexes(table=Granule))
    # and check it
    assert statement == (
        "CREATE INDEX granules_start_stop_index ON granules (start, stop);",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
