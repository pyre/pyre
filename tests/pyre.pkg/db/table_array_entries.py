#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an array column refuses a row with an entry its column type refuses, and that
declaring an array column whose entries are not a column type fires a firewall
"""


def test():
    """
    Build a row with a bad entry, and declare an array of something that is not a column type
    """
    # the journal
    import journal

    # access the package
    import pyre.db

    # a table with an array of integers
    class Grid(pyre.db.table, id="grid"):
        """
        A matrix
        """

        # the key
        id = pyre.db.int().primary()
        # and the matrix
        cells = pyre.db.array(schema=pyre.db.int(), rank=2)

    # carefully
    try:
        # build a row whose matrix has an entry that is not an integer
        Grid.pyre_immutable(id=1, cells=((1, "x"),))
    # it must be refused
    except pyre.db.array.CastingError as error:
        # naming the entry
        assert "'x'" in str(error), str(error)
    # if it is not refused at all
    else:
        # say so
        assert False, "accepted an array with a bad entry"

    # the firewall fires on purpose here; keep its report out of the way
    journal.firewall("pyre.schemata").device = journal.trash()
    # carefully
    try:
        # declare an array whose entries are a schema rather than a column type
        pyre.db.array(schema=pyre.schemata.int())
    # the firewall must fire
    except journal.FirewallError:
        # as expected
        pass
    # if it does not
    else:
        # say so
        assert False, "declared an array column of a schema"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
