#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that sqlite selects the rows whose field is among some values, and the others
"""


def test():
    """
    Store granules on three tracks, and select those on two of them and those on the third
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        # the name
        name = pyre.db.str()
        # and the track
        track = pyre.db.int()

    # the granules on the first and third tracks
    class Picked(pyre.db.query, granule=Granule):
        # their names
        name = granule.name
        # restricted
        where = pyre.db.isIn(granule.track, (1, 3))

    # and the others
    class Others(pyre.db.query, granule=Granule):
        # their names
        name = granule.name
        # restricted
        where = pyre.db.negation(pyre.db.isIn(granule.track, (1, 3)))

    # connect to a database in memory
    db = pyre.db.sqlite(name="isin").attach()
    # make the table
    db.createTable(Granule)
    # with a granule on each of three tracks
    db.insert(
        Granule.pyre_immutable(name="a", track=1),
        Granule.pyre_immutable(name="b", track=2),
        Granule.pyre_immutable(name="c", track=3),
    )
    # the granules on the first and third tracks
    picked = sorted(row.name for row in db.select(Picked))
    # are those
    assert picked == ["a", "c"], picked
    # and the others
    others = sorted(row.name for row in db.select(Others))
    # are the rest
    assert others == ["b"], others
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
