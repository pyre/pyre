#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the backup server leaves the name of its database unset until it is configured
"""


def test():
    """
    Check the default value of the name of the database of a backup server
    """
    # access the package
    import pyre.db

    # make a backup server
    server = pyre.db.backup(name="test")
    # and check that the name of its database is unset
    assert server.database is None, server.database
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
