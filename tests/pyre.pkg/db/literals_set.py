#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the literals the standard mill writes for the values a statement assigns
"""


def test():
    """
    Update a row with a truth value, an explicit {NULL} and a date, and check the statement
    """
    # support
    import datetime

    # access the package
    import pyre.db

    # a table of people
    class Person(pyre.db.table, id="persons"):
        # the key
        id = pyre.db.int().primary()
        # whether they are active
        active = pyre.db.bool()
        # their nickname
        nickname = pyre.db.str(maxlen=16)
        # and their birthday
        birthday = pyre.db.date()

    # a template that changes everything but the key
    eva = pyre.db.template(Person)
    # she is active
    eva.active = True
    # has no nickname
    eva.nickname = pyre.db.null
    # and was born on a known day
    eva.birthday = datetime.date(1930, 10, 28)

    # make a mill that speaks standard SQL
    mill = pyre.db.dialects.standard(name="literals_set")
    # build the statement that updates her row
    statement = tuple(mill.updateRecords(template=eva, condition=(Person.id == 1)))
    # and check it
    assert statement == (
        "UPDATE persons",
        "  SET",
        "    (active, nickname, birthday) = (TRUE, NULL, DATE '1930-10-28')",
        "  WHERE ((id) = (1));",
    ), statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
