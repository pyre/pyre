#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that attaching a sqlite server that is already attached hands back the server
"""


def test():
    """
    Attach twice
    """
    # access the package
    import pyre.db

    # connect to a database in memory
    db = pyre.db.sqlite(name="twice").attach()
    # attaching again is harmless, and answers like the first time
    assert db.attach() is db
    # let go
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
