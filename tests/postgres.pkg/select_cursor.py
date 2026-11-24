#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a selection is read through a cursor the session holds, which lasts while the
selection is read and is closed when it ends
"""


def test():
    """
    Start reading a table, look at the cursors of the session, finish reading, and look again
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_select_cursor"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()

    # connect
    db = pyre.db.postgres(name="select_cursor").attach()
    # make the table
    db.createTable(Granule)
    # carefully
    try:
        # add five granules
        db.insert(*(Granule.pyre_immutable(name=name) for name in "abcde"))
        # start reading them
        granules = db.select(query=Granule)
        # get the first
        next(granules)
        # while the selection is read, look at the cursors of the session
        cursors = db.execute("SELECT is_holdable FROM pg_cursors;")
        # there is one, for the selection, and it outlasts the transactions of the session
        assert [tuple(cursor) for cursor in cursors] == [(True,)], cursors
        # read the rest
        assert len(list(granules)) == 4
        # and once it is read, the cursor is gone
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
