#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a selection can be abandoned while its transaction has failed, when the session runs
nothing until the transaction rolls back
"""


def test():
    """
    Start reading a table in a transaction block, fail the transaction, abandon the selection,
    and let the block roll back
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_select_failed"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()

    # connect, fetching two rows at a time
    db = pyre.db.postgres(name="select_failed", batch=2).attach()
    # make the table
    db.createTable(Granule)
    # carefully
    try:
        # add five granules
        db.insert(*(Granule.pyre_immutable(name=name) for name in "abcde"))
        # whether the transaction failed
        failed = False
        # carefully
        try:
            # in a transaction block
            with db:
                # start reading the granules
                granules = db.select(query=Granule)
                # get the first
                next(granules)
                # carefully
                try:
                    # fail the transaction
                    db.execute("SELECT 1/0;")
                # the failure
                except pyre.db.exceptions.DataError:
                    # leaves the transaction failed; abandon the selection now, quietly
                    granules.close()
                    # and let the block roll back
                    raise
        # the end of the block
        except pyre.db.exceptions.DataError:
            # is the failure
            failed = True
        # make sure it happened
        assert failed
        # the session is fine
        assert len(list(db.select(query=Granule))) == 5
        # and holds no cursors
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
