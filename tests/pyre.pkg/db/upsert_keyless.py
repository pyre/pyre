#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an upsert into a table without a key is refused
"""


def test():
    """
    Insert into a table with no primary key, replacing existing rows, and check the refusal
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        # the key
        id = pyre.db.int()
        # and the name
        name = pyre.db.str()

    # and the journal
    import journal

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="upserts")
    # attempt to
    try:
        # build the statement
        statement = tuple(
            mill.insertRecords(Granule.pyre_immutable(id=1, name="first"), existing="replace")
        )
    # which must fail
    except journal.FirewallError as error:
        # whose report names the table
        assert "'granules'" in "\n".join(error.page), error.page
    # if it doesn't
    else:
        # the statement was built anyway
        assert False, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
