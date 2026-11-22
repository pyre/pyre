#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a template that changes nothing builds no statement
"""


def test():
    """
    Update with a template that sets no column, and check that there is no statement
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

    # a template that changes nothing
    template = pyre.db.template(Person)

    # make a mill that speaks standard SQL
    mill = pyre.db.dialects.standard(name="update_nothing")
    # build the statement
    statement = tuple(mill.updateRecords(template=template, condition=(Person.id == 1)))
    # and check that there is none
    assert statement == (), statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
