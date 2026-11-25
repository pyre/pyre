#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that sqlite refuses advisory locks, which it does not have
"""


def test():
    """
    Ask sqlite for a lock, and check it refuses
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # connect to a database in memory
    db = pyre.db.sqlite(name="lock").attach()
    # attempt to
    try:
        # take a lock
        with db.lock("tests.sqlite.pkg.sqlite_lock_refused"):
            # which must not happen
            assert False, "sqlite took a lock"
    # it fails
    except exceptions.NotSupportedError as error:
        # saying what it lacks
        assert "locks" in str(error), str(error)
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
