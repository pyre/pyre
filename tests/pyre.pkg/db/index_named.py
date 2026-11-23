#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an index takes the name it is given
"""


def test():
    """
    Declare an index with a name, and check the statement that creates it
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

    # an index with a name of its own
    Granule.pyre_index(Granule.track, name="tracks")
    # make a mill
    mill = pyre.db.backends.postgres.mill(name="indexes")
    # build the statement
    statement = tuple(mill.createIndexes(table=Granule))
    # and check it
    assert statement == ("CREATE INDEX tracks ON granules (track);",), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
