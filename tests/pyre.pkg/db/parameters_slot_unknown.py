#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that binding a statement with a value for a slot it does not have is refused, naming it
"""


def test():
    """
    Bind a restriction by a slot with a value for another, and check the refusal
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
    tuple(mill.select(query=City, parameters=parameters))
    # carefully
    try:
        # bind it with the city, and with a value for a slot it does not have
        parameters.bind(values={"city": "Chicago", "country": "USA"})
    # it must be refused
    except pyre.db.exceptions.InterfaceError as error:
        # naming the value with no slot
        assert "'country'" in str(error), str(error)
    # if it is not
    else:
        # say so
        assert False, "a statement was bound with a value for a slot it does not have"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
