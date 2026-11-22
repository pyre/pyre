#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a row built from keywords leaves the columns it does not mention without a value,
unless they were given a default
"""


def test():
    """
    Build a row that mentions only its key, and check the values of the other columns
    """
    # access the package
    import pyre.db

    # a table with a key, a column without a default, and one with a default
    class Things(pyre.db.table, id="things"):
        # the key
        id = pyre.db.int().primary()
        # the name, which has no default
        name = pyre.db.str(maxlen=16)
        # and the count, which starts at one
        count = pyre.db.int(default=1)

    # build a row that mentions only its key
    row = Things.pyre_immutable(id=7)
    # the column without a default has no value
    assert row.name is None, row.name
    # and the one with a default has it
    assert row.count == 1, row.count

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
