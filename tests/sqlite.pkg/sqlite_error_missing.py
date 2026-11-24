#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a selection from a table that does not exist is refused as a programming error, as
postgres refuses it
"""


def test():
    """
    Select from a table that was never made, and check the refusal
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
    # attempt to
    try:
        # read from the table, which was never made
        list(db.select(Reading))
    # which is refused
    except pyre.db.exceptions.ProgrammingError as error:
        # with sqlite's own name for the condition
        assert error.code == "SQLITE_ERROR", error.code
        # and its message, as it wrote it
        assert error.diagnostic == "no such table: readings", error.diagnostic
    # anything else
    else:
        # is a failure
        assert False, "the selection was not refused"
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
