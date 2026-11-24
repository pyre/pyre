#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a table names the other tables its foreign keys refer to, whether a column or the
table declares the key, once each, and leaves itself out
"""


def test():
    """
    Declare a table that refers to two others and to itself, and ask it which tables it refers to
    """
    # access the package
    import pyre.db

    # a table of missions
    class Mission(pyre.db.table, id="missions"):
        """
        Missions
        """

        # the name
        name = pyre.db.str().primary()

    # a table of instruments
    class Instrument(pyre.db.table, id="instruments"):
        """
        Instruments
        """

        # the name
        name = pyre.db.str().primary()

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()
        # the mission, a reference the column declares
        mission = pyre.db.str().references(key=Mission.name)
        # the instrument
        instrument = pyre.db.str()
        # and the granule it was made from
        parent = pyre.db.str()

    # the reference to the instrument, which the table declares
    Granule.pyre_foreignKey(field=Granule.instrument, foreign=Instrument.name)
    # the one to the granule it was made from, which refers to the table itself
    Granule.pyre_foreignKey(field=Granule.parent, foreign=Granule.name)
    # and another to the mission, which it already refers to
    Granule.pyre_foreignKey(field=Granule.mission, foreign=Mission.name)

    # the tables the granules refer to, in the order of their declaration
    assert Granule.pyre_referencedTables() == (Mission, Instrument)
    # and a table without foreign keys refers to none
    assert Mission.pyre_referencedTables() == ()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
