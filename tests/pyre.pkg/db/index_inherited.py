#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a derived table inherits the indexes of its base, under its own name
"""


def test():
    """
    Derive a table from one with an index, and check the index of the derived table
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

    # a table of the granules that were reprocessed
    class Reprocessed(Granule, id="reprocessed"):
        # the version of the processor
        version = pyre.db.str()

    # make a mill
    mill = pyre.db.backends.postgres.mill(name="indexes")
    # build the statement
    statement = tuple(mill.createIndexes(table=Reprocessed))
    # and check it
    assert statement == (
        "CREATE INDEX reprocessed_start_stop_index ON reprocessed (start, stop);",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
