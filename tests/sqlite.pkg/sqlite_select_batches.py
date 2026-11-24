#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a selection fetched a few rows at a time hands back every row, whether or not their
number is a multiple of the batch
"""


def test():
    """
    Read a table two rows at a time, as it grows from none to five rows
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

    # connect to a database in memory, fetching two rows at a time
    db = pyre.db.sqlite(name="select_batches", batch=2).attach()
    # make the table
    db.createTable(Granule)
    # the names of the granules
    names = "abcde"
    # for each size of the table
    for count in range(len(names) + 1):
        # read it
        granules = sorted(granule.name for granule in db.select(query=Granule))
        # and check that every granule came back
        assert granules == list(names[:count]), (count, granules)
        # then grow it, while there are names left
        if count < len(names):
            # by one granule
            db.insert(Granule.pyre_immutable(name=names[count]))
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
