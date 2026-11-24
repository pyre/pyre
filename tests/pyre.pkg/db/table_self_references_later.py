#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a table may be made without its references to itself, which are added once its rows
are in, and with its references to other tables
"""


def test():
    """
    Declare a table that refers to itself and to another table, and make it without the first
    """
    # access the package
    import pyre.db

    # a table of missions
    class Mission(pyre.db.table, id="missions"):
        """
        Missions
        """

        # the key
        label = pyre.db.int().primary()

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        """
        Granules
        """

        # the key
        label = pyre.db.int().primary()
        # the granule it was derived from
        parent = pyre.db.int()
        # and its mission
        mission = pyre.db.int()

    # each granule may be derived from another
    Granule.pyre_foreignKey(field=Granule.parent, foreign=Granule.label, name="lineage")
    # and belongs to a mission
    Granule.pyre_foreignKey(field=Granule.mission, foreign=Mission.label, name="owner")

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="table_self_references_later")
    # build the statement that makes the table, without its references to itself
    statement = tuple(mill.createTable(table=Granule, selfReferences=False))
    # it leaves out the reference to itself
    assert not any("lineage" in line for line in statement), statement
    # and keeps the one to the missions
    assert any("CONSTRAINT owner" in line for line in statement), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
