#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a selection abandoned before its last row leaves no cursor in the session
"""


def test():
    """
    Read the first row of a table, abandon the rest, and look at the cursors of the session
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_select_abandoned"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()

    # connect, fetching two rows at a time
    db = pyre.db.postgres(name="select_abandoned", batch=2).attach()
    # make the table
    db.createTable(Granule)
    # carefully
    try:
        # add five granules
        db.insert(*(Granule.pyre_immutable(name=name) for name in "abcde"))
        # go through them
        for granule in db.select(query=Granule):
            # but stop after the first
            break
        # the cursor of the selection is gone
        assert len(db.execute("SELECT name FROM pg_cursors;")) == 0
    # either way
    finally:
        # leave nothing behind
        db.dropTable(Granule)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
