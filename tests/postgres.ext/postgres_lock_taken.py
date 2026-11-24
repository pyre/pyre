#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a session cannot take a lock another session holds
"""


def test():
    """
    Hold a lock in one session, and try to take it from another without waiting
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # one session
    first = pyre.db.postgres(name="lock_holder").attach()
    # and another
    second = pyre.db.postgres(name="lock_taker").attach()
    # the first session takes the lock
    with first.lock("pyre.tests.lock"):
        # attempt to
        try:
            # take it from the other session
            with second.lock("pyre.tests.lock", wait=False):
                # which must not happen
                assert False, "two sessions held the same lock"
        # it fails
        except exceptions.LockError as error:
            # naming the lock
            assert "pyre.tests.lock" in str(error), str(error)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
