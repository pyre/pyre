#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that each dialect quotes the words it reserves: user is reserved in postgres, not in sqlite
"""


def test():
    """
    Render the same word in the dialects of postgres and sqlite, and compare
    """
    # access the package
    import pyre.db

    # make a mill
    mill = pyre.db.backends.postgres.mill(name="identifiers")
    # render the name
    text = mill.identifier("user")
    # and check that postgres quotes it
    assert text == '"user"', text
    # while sqlite, which does not reserve it, leaves it alone
    assert pyre.db.backends.sqlite.mill(name="plain").identifier("user") == "user"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
