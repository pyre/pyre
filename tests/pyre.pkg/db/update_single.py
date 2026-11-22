#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the statement that updates a single column
"""


def test():
    """
    Update the phone number of one person, and check the statement
    """
    # access the package
    import pyre.db

    # a table of people
    class Person(pyre.db.table, id="persons"):
        # the key
        id = pyre.db.int().primary()
        # their name
        name = pyre.db.str(maxlen=16)
        # and their phone number
        phone = pyre.db.str(maxlen=16)

    # a template that changes only the phone number
    template = pyre.db.template(Person)
    # to a new one
    template.phone = "555 1212"

    # make a mill that speaks standard SQL
    mill = pyre.db.dialects.standard(name="update_single")
    # build the statement
    statement = tuple(mill.updateRecords(template=template, condition=(Person.id == 1)))
    # and check it
    assert statement == (
        "UPDATE persons",
        "  SET",
        "    phone = '555 1212'",
        "  WHERE ((id) = (1));",
    ), statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
