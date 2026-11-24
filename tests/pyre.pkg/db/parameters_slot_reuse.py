#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a slot that appears twice in a statement over postgres takes one placeholder
"""


def test():
    """
    Restrict a query by one slot in two places, and check both use the same placeholder
    """
    # access the package
    import pyre.db

    # a table of trips
    class Trip(pyre.db.table, id="trips"):
        # where it started
        origin = pyre.db.str()
        # and where it ended
        destination = pyre.db.str()

    # the city that is given when the statement runs
    city = pyre.db.parameter(name="city", schema=pyre.db.str())

    # the trips that touch it
    class Touching(pyre.db.query, trip=Trip):
        # where they started
        origin = trip.origin
        # the restriction
        where = (trip.origin == city) | (trip.destination == city)

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="parameters")
    # and a place for the values of a statement
    parameters = mill.parameters()
    # build the statement
    statement = "\n".join(mill.select(query=Touching, parameters=parameters))
    # both comparisons use the same placeholder
    assert statement.count("CAST($1 AS TEXT)") == 2, statement
    # and there is no other
    assert "$2" not in statement, statement
    # the slot is kept once
    assert tuple(parameters.slots()) == (("city", 1),), parameters.slots()
    # and binding fills it once
    assert parameters.bind(values={"city": "Pasadena"}) == ("Pasadena",)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
