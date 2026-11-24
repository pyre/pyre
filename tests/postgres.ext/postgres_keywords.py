#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the dialect of postgres knows every word the server reserves
"""


def test():
    """
    Compare the reserved words of the dialect with those the live server reports
    """
    # access the package
    import pyre.db

    # connect
    db = pyre.db.postgres(name="keywords").attach()
    # ask the server for the words a name must be quoted to use
    rows = db.execute("SELECT word FROM pg_get_keywords() WHERE catcode IN ('R', 'T')")
    # collect them
    words = {word for (word,) in rows}
    # the dialect's own list
    reserved = pyre.db.backends.postgres.mill(name="keywords").reserved
    # must hold every one of them
    missing = sorted(words - reserved)
    # or names made of them would not be quoted
    assert not missing, missing
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
