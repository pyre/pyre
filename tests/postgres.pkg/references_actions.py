#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the server carries out the actions a reference declares, when the row it refers to
changes its key or goes away
"""


def test():
    """
    Renumber the location of one measurement and remove the location of another, and read where
    each measurement ended up
    """
    # access the package
    import pyre.db

    # a table of locations
    class Location(pyre.db.table, id="pyre_references_actions_locations"):
        """
        Locations
        """

        # the key
        id = pyre.db.int().primary()

    # a table of measurements, each at a location
    class Measurement(pyre.db.table, id="pyre_references_actions_measurements"):
        """
        Measurements
        """

        # the key
        id = pyre.db.int().primary()
        # the location, which goes back to the unknown one when its key changes, and becomes
        # null when it goes away
        location = pyre.db.int(default=0).references(
            key=Location.id, onDelete=pyre.db.setNull, onUpdate=pyre.db.setDefault
        )

    # connect
    db = pyre.db.postgres(name="references_actions").attach()
    # make the table of locations
    db.createTable(Location)
    # carefully
    try:
        # make the table of measurements, which refers to it
        db.createTable(Measurement)
        # carefully
        try:
            # the unknown location, and two others
            db.insert(*(Location.pyre_immutable(id=id) for id in (0, 1, 2)))
            # a measurement at each of the two
            db.insert(
                Measurement.pyre_immutable(id=1, location=1),
                Measurement.pyre_immutable(id=2, location=2),
            )

            # a template that renumbers a location
            template = pyre.db.template(Location)
            template.id = 10
            # renumber the first location
            db.update((template, Location.id == 1))
            # and remove the second
            db.delete(table=Location, condition=Location.id == 2)

            # read where the measurements ended up
            locations = {row.id: row.location for row in db.select(Measurement)}
            # the first went back to the unknown location, and the second lost its location
            assert locations == {1: 0, 2: None}, locations
        # either way
        finally:
            # leave nothing behind: neither the measurements
            db.dropTable(Measurement)
    # either way
    finally:
        # nor the locations
        db.dropTable(Location)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
