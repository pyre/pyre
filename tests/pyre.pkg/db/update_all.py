#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the statement that updates every row of a table
"""


def test():
    """
    Update the name and phone number of everybody, and check the statement
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

    # a template that changes the name
    template = pyre.db.template(Person)
    # to nobody in particular
    template.name = "anonymous"
    # and clears the phone number
    template.phone = pyre.db.null

    # make a mill that speaks standard SQL
    mill = pyre.db.dialects.standard(name="update_all")
    # build the statement, with no condition
    statement = tuple(mill.updateRecords(template=template, condition=None))
    # and check that it has no restriction
    assert statement == (
        "UPDATE persons",
        "  SET",
        "    name = 'anonymous',",
        "    phone = NULL;",
    ), statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
