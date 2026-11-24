#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that records of two shapes are inserted by two statements, each with its own values
"""


def test():
    """
    Insert records that name different columns, one statement at a time, and check each
    statement numbers its placeholders from the first
    """
    # access the package
    import pyre.db

    # a table of readings
    class Reading(pyre.db.table, id="readings"):
        # the city
        city = pyre.db.str()
        # and how many there were
        count = pyre.db.int()

    # and a table of cities
    class City(pyre.db.table, id="cities"):
        # the name
        name = pyre.db.str()

    # a reading and a city, which take statements of their own
    records = (
        Reading.pyre_immutable(city="Chicago", count=3),
        City.pyre_immutable(name="Boston"),
    )
    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="parameters")
    # and a place for the values of a statement
    parameters = mill.parameters()
    # the statements, with their values
    statements = []
    # built one at a time
    for statement in mill.insertStatements(*records, parameters=parameters):
        # each with the values collected once it is whole
        statements.append((statement[-1], parameters.drain()))
    # there are two of them
    assert len(statements) == 2, statements
    # the first holds the values of the reading
    assert statements[0] == ("    ($1, $2);", ("Chicago", 3)), statements[0]
    # and the second numbers its own from the first
    assert statements[1] == ("    ($1);", ("Boston",)), statements[1]
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
