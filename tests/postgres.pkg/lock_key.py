#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the key of a lock is the first eight bytes of the BLAKE2b digest of its name
"""


def test():
    """
    Take a lock, and find its key among the locks postgres holds
    """
    # support
    import hashlib

    # access the package
    import pyre.db

    # connect
    db = pyre.db.postgres(name="lock_key").attach()
    # the key, as pyre.db computes it
    digest = hashlib.blake2b("tests.postgres.pkg.lock_key".encode("utf-8"), digest_size=8).digest()
    # and as a signed integer of 64 bits
    key = int.from_bytes(digest, "big", signed=True)
    # postgres splits it into its two halves
    high, low = (key >> 32) & 0xFFFFFFFF, key & 0xFFFFFFFF
    # take the lock
    with db.lock("tests.postgres.pkg.lock_key"):
        # and look for it among the advisory locks of this session
        rows = db.execute(
            "SELECT classid, objid FROM pg_locks"
            " WHERE locktype = 'advisory' AND pid = pg_backend_pid()"
        )
        # the halves of the key
        held = [(int(classid), int(objid)) for classid, objid in rows]
        # are those of the key
        assert held == [(high, low)], (held, (high, low))
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
