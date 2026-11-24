#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a prepared delete removes the rows its slots pick, and hands them back with
{returning}
"""


def test():
    """
    Prepare the removal of a granule by name that returns it, and run it for two names
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_prepare_delete"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()
        # and the size
        size = pyre.db.int()

    # connect
    db = pyre.db.postgres(name="prepare_delete").attach()
    # make the table
    db.createTable(Granule)
    # carefully
    try:
        # add three granules
        db.insert(
            *(Granule.pyre_immutable(name=name, size=index) for index, name in enumerate("abc"))
        )
        # prepare the removal of the granule whose name is given when the statement runs
        drop = db.prepareDelete(
            table=Granule,
            condition=Granule.name == pyre.db.parameter(name="name", schema=pyre.db.str()),
            returning=Granule,
        )
        # remove the first, which comes back
        assert [(row.name, row.size) for row in drop.run(name="a")] == [("a", 0)]
        # and the last
        assert [(row.name, row.size) for row in drop.run(name="c")] == [("c", 2)]
        # read what is left
        names = [row.name for row in db.select(Granule)]
        # only the other one
        assert names == ["b"], names
    # either way
    finally:
        # leave nothing behind
        db.dropTable(Granule)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
