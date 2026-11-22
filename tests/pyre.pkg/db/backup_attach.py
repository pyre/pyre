#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that attaching a backup server hands back the server
"""


def test():
    """
    Attach a backup server, and check what comes back
    """
    # access the package
    import pyre.db

    # make a server
    db = pyre.db.backup(name="backup_attach")
    # attaching it hands it back, so it can be chained
    assert db.attach() is db
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
