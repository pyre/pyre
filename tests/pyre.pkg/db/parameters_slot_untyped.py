#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a slot without a type, where no column gives it one, is a mistake in the code that
declared it
"""


def test():
    """
    Restrict a query by a slot that says nothing about its type, and check the firewall
    """
    # the journal
    import journal

    # access the package
    import pyre.db

    # a table of readings
    class Reading(pyre.db.table, id="readings"):
        # the city
        city = pyre.db.str()
        # and how many there were
        count = pyre.db.int()

    # the readings of a city named by a slot that does not say what it holds
    class City(pyre.db.query, reading=Reading):
        # the count
        count = reading.count
        # the restriction
        where = reading.city == pyre.db.parameter(name="city")

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="parameters")
    # the firewall fires on purpose here; keep its report out of the way
    journal.firewall("pyre.db").device = journal.trash()
    # carefully
    try:
        # build the statement
        tuple(mill.select(query=City, parameters=mill.parameters()))
    # the firewall must fire
    except journal.FirewallError as error:
        # whose report names the slot
        assert "'city'" in "\n".join(error.page), error.page
    # if it does not
    else:
        # say so
        assert False, "a slot without a type was rendered in a restriction"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
