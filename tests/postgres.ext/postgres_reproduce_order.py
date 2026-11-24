#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a postgres server reproduces a table before the tables that refer to it, whatever the
order it is given them in
"""


def test():
    """
    Reproduce granules and the missions they refer to, given the granules first
    """
    # access the package
    import pyre.db

    # a table of missions
    class Mission(pyre.db.table, id="pyre_reproduce_order_missions"):
        """
        Missions
        """

        # the name
        name = pyre.db.str().primary()

    # a table of granules
    class Granule(pyre.db.table, id="pyre_reproduce_order_granules"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()
        # and the mission
        mission = pyre.db.str().references(key=Mission.name)

    # the source, a sqlite database in memory
    source = pyre.db.sqlite(name="reproduce_order_source").attach()
    # with the table of missions
    source.createTable(Mission)
    # and the one of granules
    source.createTable(Granule)
    # a mission
    source.insert(Mission.pyre_immutable(name="nisar"))
    # and two of its granules
    source.insert(*(Granule.pyre_immutable(name=name, mission="nisar") for name in "ab"))
    # the target
    target = pyre.db.postgres(name="reproduce_order").attach()
    # carefully
    try:
        # reproduce the tables, given the one that refers to the other first
        target.reproduce(source=source, tables=(Granule, Mission))
        # the granules are there
        assert sorted(row.name for row in target.select(query=Granule)) == ["a", "b"]
    # either way
    finally:
        # leave nothing behind: neither the granules
        target.dropTable(Granule, missingOk=True)
        # nor the missions
        target.dropTable(Mission, missingOk=True)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
