#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the end of a block releases its lock
"""


def test():
    """
    Take a lock in one session and let the block end, then take it from another
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # one session
    first = pyre.db.postgres(name="lock_first").attach()
    # and another
    second = pyre.db.postgres(name="lock_second").attach()
    # the first session takes the lock, and lets go of it
    with first.lock("tests.postgres.pkg.lock_released"):
        # with nothing in between
        pass
    # the second session takes it without waiting
    with second.lock("tests.postgres.pkg.lock_released", wait=False):
        # which it does
        pass
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
