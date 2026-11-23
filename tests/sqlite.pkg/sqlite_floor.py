#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the sqlite python is linked against has every feature pyre.db uses
"""


def test():
    """
    Ask the dialect of sqlite whether its library returns rows and meets the rows that are
    there already
    """
    # access the package
    import pyre.db

    # make a mill that speaks the dialect of sqlite
    mill = pyre.db.backends.sqlite.mill(name="floor")
    # the library is at least as recent as the floor of pyre.db
    assert mill.version >= (3, 35), mill.version
    # so statements may return the rows they change
    assert mill.hasReturning, mill.version
    # and inserts may meet the rows that are there already
    assert mill.hasConflict, mill.version
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
