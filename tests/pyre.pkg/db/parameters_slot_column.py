#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a slot in the template of an update over postgres is a bare placeholder, typed by its
column, and that its value takes the type of the column when the statement is bound
"""


def test():
    """
    Update the count a slot holds, and bind it next to the constant of the restriction
    """
    # access the package
    import pyre.db

    # a table of readings
    class Reading(pyre.db.table, id="readings"):
        # the city
        city = pyre.db.str()
        # and how many there were
        count = pyre.db.int()

    # a template whose count is given when the statement runs; the column gives the slot its type
    template = pyre.db.template(Reading)
    template.count = pyre.db.parameter(name="count")
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
    # the new value is a bare placeholder
    assert "    count = $1" in statement, statement
    # and the constant of the restriction comes after it
    assert statement[-1].endswith("(CAST($2 AS TEXT)));"), statement[-1]
    # the slot is kept, by name, with its placeholder
    assert tuple(parameters.slots()) == (("count", 1),), parameters.slots()
    # binding fills the slot, with the value converted to the type of the column
    assert parameters.bind(values={"count": "7"}) == (7, "Chicago")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
