#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a session gives up waiting for a lock after its timeout
"""


def test():
    """
    Hold a lock in one session, and wait for it in another for a fraction of a second
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # one session
    first = pyre.db.postgres(name="lock_keeper").attach()
    # and another
    second = pyre.db.postgres(name="lock_waiter").attach()
    # support
    import time

    # the first session takes the lock
    with first.lock("pyre.tests.lock"):
        # note the time
        start = time.monotonic()
        # attempt to
        try:
            # take it from the other session
            with second.lock("pyre.tests.lock", timeout=0.2):
                # which must not happen
                assert False, "two sessions held the same lock"
        # it fails
        except exceptions.LockError as error:
            # naming the lock
            assert "pyre.tests.lock" in str(error), str(error)
        # and the wait was the timeout, not forever
        assert time.monotonic() - start < 5, time.monotonic() - start
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
