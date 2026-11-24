#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a string of octets is stored and read back as the same octets
"""


def test():
    """
    Store octets that include a zero, a quote and a backslash, and read them back
    """
    # access the package
    import pyre.db

    # a table of opaque payloads
    class Blob(pyre.db.table, id="pyre_bytes"):
        """
        Opaque payloads
        """

        # the key
        id = pyre.db.int().primary()
        # the payload
        payload = pyre.db.bytes()

    # connect
    db = pyre.db.postgres(name="octets").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Blob)
        # ask what the column holds
        kind = db.execute(
            "SELECT data_type FROM information_schema.columns"
            " WHERE table_name = 'pyre_bytes' AND column_name = 'payload'"
        )[0][0]
        # it must be a string of octets
        assert kind == "bytea", kind
        # pick some octets that are awkward to quote
        payload = b"\x00\xff'\\ab"
        # store it
        db.insert(Blob.pyre_immutable(id=1, payload=payload))
        # and read it back
        (row,) = db.select(Blob)
        # they are the same octets
        assert row.payload == payload, row.payload
    # either way
    finally:
        # leave nothing behind
        db.execute("ROLLBACK")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
