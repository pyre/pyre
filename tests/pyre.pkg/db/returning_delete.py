#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres asks a deletion for the rows it removes with RETURNING
"""


def test():
    """
    Delete a granule, asking for its whole row, and check the statement
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        # the key
        id = pyre.db.int().primary()
        # and the name
        name = pyre.db.str()

    # make a mill
    mill = pyre.db.backends.postgres.mill(name="returning")
    # build the statement
    statement = tuple(
        mill.deleteRecords(table=Granule, condition=Granule.id == 2, returning=Granule)
    )
    # and check it
    assert statement == (
        "DELETE FROM granules",
        "  WHERE ((id) = (2))",
        "  RETURNING id, name;",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
