#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a block that raises releases its lock
"""


def test():
    """
    Take a lock in one session in a block that raises, then take it from another
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # one session
    first = pyre.db.postgres(name="lock_raiser").attach()
    # and another
    second = pyre.db.postgres(name="lock_after").attach()
    # attempt to
    try:
        # hold the lock
        with first.lock("pyre.tests.lock"):
            # in a block that fails
            raise ValueError("give up")
    # absorb the failure
    except ValueError:
        # and move on
        pass
    # the second session takes the lock without waiting
    with second.lock("pyre.tests.lock", wait=False):
        # which it does
        pass
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
