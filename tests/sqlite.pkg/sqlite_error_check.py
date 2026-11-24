#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a row a check refuses is refused with pyre.db's exception, and sqlite's message
"""


def test():
    """
    Insert a row with a negative count, and check the refusal names the check as sqlite wrote it
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
    # attempt to
    try:
        # write a row the check refuses
        db.insert(Reading.pyre_immutable(id=1, count=-1))
    # which is refused
    except pyre.db.exceptions.IntegrityError as error:
        # with sqlite's own name for the condition
        assert error.code == "SQLITE_CONSTRAINT_CHECK", error.code
        # and its message, as it wrote it
        assert error.diagnostic == "CHECK constraint failed: positive", error.diagnostic
    # anything else
    else:
        # is a failure
        assert False, "the row was not refused"
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
