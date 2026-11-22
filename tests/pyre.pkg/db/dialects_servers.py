#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that each server speaks the dialect of its back end, and the backup server standard SQL
"""


def test():
    """
    Make one of each server, and check the mill it speaks by default
    """
    # access the package
    import pyre.db

    # each server, and the mill it speaks
    expectations = [
        # postgres speaks its own dialect
        (pyre.db.postgres, pyre.db.backends.postgres.mill),
        # and so does sqlite
        (pyre.db.sqlite, pyre.db.backends.sqlite.mill),
        # the backup server records statements for any back end, so it speaks the standard
        (pyre.db.backup, pyre.db.backends.standard.mill),
    ]
    # go through them
    for server, mill in expectations:
        # make one
        instance = server(name=f"dialects.{server.__name__.lower()}")
        # and check its mill
        assert type(instance.sql) is mill, (server, type(instance.sql))
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
