#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a selection with a slot is refused unless it is prepared, naming the slot, before
anything reaches the database
"""


def test():
    """
    Select through a query with a slot, without preparing it
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()
        # and the size
        size = pyre.db.int()

    # the size of the granule whose name is given when the statement runs
    class Lookup(pyre.db.query, granule=Granule):
        """
        The size of one granule
        """

        # the size
        size = granule.size
        # the restriction
        where = granule.name == pyre.db.parameter(name="name", schema=pyre.db.str())

    # connect to a database in memory
    db = pyre.db.sqlite(name="select_slot").attach()
    # make the table
    db.createTable(Granule)
    # carefully
    try:
        # select through the query as it is
        list(db.select(Lookup))
    # it must be refused
    except pyre.db.exceptions.InterfaceError as error:
        # naming the slot
        assert "'name'" in str(error), str(error)
    # if it is not
    else:
        # say so
        assert False, "a selection with a slot ran without being prepared"
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
