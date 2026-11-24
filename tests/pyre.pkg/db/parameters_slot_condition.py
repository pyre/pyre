#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a slot in a restriction over postgres is a placeholder cast to the type of the slot,
and that it keeps no value
"""


def test():
    """
    Restrict a query to the city a slot names, and check its placeholder and the slots kept
    """
    # access the package
    import pyre.db

    # a table of readings
    class Reading(pyre.db.table, id="readings"):
        # the city
        city = pyre.db.str()
        # and how many there were
        count = pyre.db.int()

    # the readings of the city that is given when the statement runs
    class City(pyre.db.query, reading=Reading):
        # the count
        count = reading.count
        # the restriction
        where = reading.city == pyre.db.parameter(name="city", schema=pyre.db.str())

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="parameters")
    # and a place for the values of a statement
    parameters = mill.parameters()
    # build the statement
    statement = tuple(mill.select(query=City, parameters=parameters))
    # the restriction holds a placeholder that says what the value is
    assert statement[-1] == "    ((reading.city) = (CAST($1 AS TEXT)));", statement[-1]
    # the slot is kept, by name, with its placeholder
    assert tuple(parameters.slots()) == (("city", 1),), parameters.slots()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
