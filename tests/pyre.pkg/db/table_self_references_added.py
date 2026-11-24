#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the references of a table to itself are added to the table, one statement each,
and its references to other tables are not
"""


def test():
    """
    Declare a table that refers to itself and to another table, and add the first
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
        # the granule it replaces
        replaces = pyre.db.int()
        # and its mission
        mission = pyre.db.int()

    # each granule may be derived from another
    Granule.pyre_foreignKey(field=Granule.parent, foreign=Granule.label, name="lineage")
    # and may replace another
    Granule.pyre_foreignKey(field=Granule.replaces, foreign=Granule.label)
    # and belongs to a mission
    Granule.pyre_foreignKey(field=Granule.mission, foreign=Mission.label, name="owner")

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="table_self_references_added")
    # build the statements that add the references of the table to itself
    statements = tuple(mill.addSelfReferences(table=Granule))
    # and check them
    assert statements == (
        "ALTER TABLE granules ADD CONSTRAINT lineage FOREIGN KEY (parent) REFERENCES granules (label);",
        "ALTER TABLE granules ADD FOREIGN KEY (replaces) REFERENCES granules (label);",
    ), statements
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
