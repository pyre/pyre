#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a failure sqlite reports while a selection is read, after its statement was sent, is
reported with the exceptions of the package
"""


def test():
    """
    Read a table one row at a time, interrupt sqlite after the first row, and check what the rest
    of the reading raises
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

    # connect to a database in memory, fetching one row at a time
    db = pyre.db.sqlite(name="select_interrupted", batch=1).attach()
    # make the table
    db.createTable(Granule)
    # with five granules
    db.insert(*(Granule.pyre_immutable(name=name) for name in "abcde"))
    # start reading them
    granules = db.select(query=Granule)
    # get the first
    next(granules)
    # interrupt sqlite, which fails the statement that is being read
    db.connection.interrupt()
    # carefully
    try:
        # read the rest
        list(granules)
    # the failure
    except pyre.db.exceptions.OperationalError as error:
        # is the interruption, named as sqlite names it
        assert error.code == "SQLITE_INTERRUPT", error.code
    # reading to the end
    else:
        # means the interruption was lost
        assert False, "the interruption was not reported"
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
