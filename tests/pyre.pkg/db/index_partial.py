#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the statement postgres builds for an index over some of the rows
"""


def test():
    """
    Declare an index over the rows that pass a predicate, and check the statement
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

    # index the granules whose track is known
    Granule.pyre_index(Granule.track, where=pyre.db.isNotNull(Granule.track))
    # make a mill
    mill = pyre.db.backends.postgres.mill(name="indexes")
    # build the statement
    statement = tuple(mill.createIndexes(table=Granule))
    # and check it
    assert statement == (
        "CREATE INDEX granules_track_index ON granules (track) WHERE (track IS NOT NULL);",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
