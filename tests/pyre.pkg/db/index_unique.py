#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the statement postgres builds for a unique index
"""


def test():
    """
    Declare a unique index, and check the statement that creates it
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

    # no two granules share a name
    Granule.pyre_index(Granule.name, unique=True)
    # make a mill
    mill = pyre.db.backends.postgres.mill(name="indexes")
    # build the statement
    statement = tuple(mill.createIndexes(table=Granule))
    # and check it
    assert statement == ("CREATE UNIQUE INDEX granules_name_index ON granules (name);",), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
