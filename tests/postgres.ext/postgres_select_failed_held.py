#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a selection begun outside a transaction, and abandoned while a transaction has failed,
has its cursor closed by the next selection, since the rollback leaves it to the session
"""


def test():
    """
    Start reading a table, fail a transaction, abandon the selection, and read the table again
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_select_failed_held"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()

    # connect, fetching two rows at a time
    db = pyre.db.postgres(name="select_failed_held", batch=2).attach()
    # make the table
    db.createTable(Granule)
    # carefully
    try:
        # add five granules
        db.insert(*(Granule.pyre_immutable(name=name) for name in "abcde"))
        # start reading them, outside a transaction
        granules = db.select(query=Granule)
        # get the first
        next(granules)
        # whether the transaction failed
        failed = False
        # carefully
        try:
            # in a transaction block
            with db:
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
        # the rollback left the cursor of the selection to the session
        assert len(db.execute("SELECT name FROM pg_cursors;")) == 1
        # the next selection reads every granule
        assert len(list(db.select(query=Granule))) == 5
        # and closes the cursor that was left behind
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
