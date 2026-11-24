#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an update over postgres sends its new values and its restriction as parameters
"""


def test():
    """
    Update the count of one city, and check the placeholders and the values, in order
    """
    # access the package
    import pyre.db

    # a table of readings
    class Reading(pyre.db.table, id="readings"):
        # the city
        city = pyre.db.str()
        # the day of the reading
        day = pyre.db.date()
        # and how many there were
        count = pyre.db.int()

    # a template that changes the count
    template = pyre.db.template(Reading)
    template.count = 7
    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="parameters")
    # and a place for the values of a statement
    parameters = mill.parameters()
    # build the statement
    statement = tuple(
        mill.updateRecords(
            template=template, condition=(Reading.city == "Chicago"), parameters=parameters
        )
    )
    # the new value takes the type of its column, and the restriction says what its value is
    assert "    count = $1" in statement, statement
    # the restriction comes last
    assert statement[-1].endswith("(CAST($2 AS TEXT)));"), statement[-1]
    # and the values travel in the order of their placeholders
    assert parameters.drain() == (7, "Chicago")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
