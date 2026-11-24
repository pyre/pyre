#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a selection started in a transaction that rolls back can be abandoned afterwards,
once the rollback has taken its cursor
"""


def test():
    """
    Start reading a table in a transaction block that raises, then abandon the selection
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_select_rollback"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()

    # the exception that ends the block
    class Stop(Exception):
        """
        Exception raised to end the transaction block
        """

    # connect, fetching two rows at a time
    db = pyre.db.postgres(name="select_rollback", batch=2).attach()
    # make the table
    db.createTable(Granule)
    # carefully
    try:
        # add five granules
        db.insert(*(Granule.pyre_immutable(name=name) for name in "abcde"))
        # the selection
        granules = None
        # carefully
        try:
            # in a transaction block
            with db:
                # start reading the granules
                granules = db.select(query=Granule)
                # get the first
                next(granules)
                # and end the block, which rolls back the transaction
                raise Stop()
        # the end of the block
        except Stop:
            # leaves the selection behind, without its cursor
            assert granules is not None
        # abandon the selection, quietly
        granules.close()
        # the session is fine
        assert len(list(db.select(query=Granule))) == 5
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
