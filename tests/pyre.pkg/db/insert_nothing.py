#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an insert with no records builds no statement
"""


def test():
    """
    Ask for the statement that inserts no records, and check that there is none
    """
    # access the package
    import pyre.db

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="insert_nothing")
    # build the statement
    statement = tuple(mill.insertRecords())
    # and check that there is none
    assert statement == (), statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
