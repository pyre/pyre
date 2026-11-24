#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a row whose key is taken is refused with pyre.db's exception, which names the
condition the way sqlite does
"""


def test():
    """
    Insert two rows with the same key, and check the second is refused as an integrity error
    """
    # access the package
    import pyre.db

    # a table of readings
    class Reading(pyre.db.table, id="readings"):
        # the key
        id = pyre.db.int().primary()
        # and the count, which is never negative
        count = pyre.db.int()

    # with a check that says so
    Reading.pyre_check(Reading.count >= 0, name="positive")

    # connect to a database in memory
    db = pyre.db.sqlite(name="errors").attach()
    # make the table
    db.createTable(Reading)
    # write a row
    db.insert(Reading.pyre_immutable(id=1, count=3))
    # attempt to
    try:
        # write another with the same key
        db.insert(Reading.pyre_immutable(id=1, count=4))
    # which is refused
    except pyre.db.exceptions.IntegrityError as error:
        # with sqlite's own name for the condition
        assert error.code == "SQLITE_CONSTRAINT_PRIMARYKEY", error.code
        # no sqlstate, which sqlite does not have
        assert error.sqlstate == "", error.sqlstate
        # and the statement that provoked it
        assert error.command.startswith("INSERT INTO readings"), error.command
    # anything else
    else:
        # is a failure
        assert False, "the second row was not refused"
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
