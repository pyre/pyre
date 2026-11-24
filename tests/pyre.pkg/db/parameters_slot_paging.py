#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the bounds of a selection over postgres may be slots, whose placeholders are numbered
in the order they appear in the statement
"""


def test():
    """
    Page through the readings of a city, with the city and both bounds given as slots
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
    # build the statement, with slots for its bounds
    statement = tuple(
        mill.select(
            query=City,
            offset=pyre.db.parameter(name="offset"),
            limit=pyre.db.parameter(name="limit"),
            parameters=parameters,
        )
    )
    # the restriction comes first
    assert "    ((reading.city) = (CAST($1 AS TEXT)))" in statement, statement
    # then the rows to skip
    assert "  OFFSET $2 ROWS" in statement, statement
    # and then the rows to keep
    assert statement[-1] == "  FETCH FIRST $3 ROWS ONLY;", statement[-1]
    # the slots are kept in that order
    assert tuple(parameters.slots()) == (("city", 1), ("offset", 2), ("limit", 3))
    # and binding makes integers of the bounds
    assert parameters.bind(values={"city": "Chicago", "offset": "10", "limit": 5}) == (
        "Chicago",
        10,
        5,
    )
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
