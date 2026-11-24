#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a prepared delete removes the rows its slots pick, and only those
"""


def test():
    """
    Prepare the removal of a granule by name, and run it for two names
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()
        # and the size
        size = pyre.db.int()

    # connect to a database in memory
    db = pyre.db.sqlite(name="prepare_delete").attach()
    # make the table
    db.createTable(Granule)
    # with three granules
    db.insert(*(Granule.pyre_immutable(name=name, size=0) for name in "abc"))
    # prepare the removal of the granule whose name is given when the statement runs
    drop = db.prepareDelete(
        table=Granule,
        condition=Granule.name == pyre.db.parameter(name="name", schema=pyre.db.str()),
    )
    # remove the first
    drop.run(name="a")
    # and the last
    drop.run(name="c")
    # read what is left
    names = sorted(row.name for row in db.select(Granule))
    # only the other one
    assert names == ["b"], names
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
