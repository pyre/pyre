#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a selection can be abandoned after its server has hung up, which took its cursor
with the session
"""


def test():
    """
    Start reading a table, detach the server, attach it again, and abandon the selection
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_select_detached"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()

    # connect, fetching two rows at a time
    db = pyre.db.postgres(name="select_detached", batch=2).attach()
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
        # hang up, which takes the cursor with the session
        db.detach()
        # and connect again
        db.attach()
        # abandon the selection, quietly
        granules.close()
        # the new session is fine
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
