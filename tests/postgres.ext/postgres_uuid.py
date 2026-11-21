#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a universally unique identifier is stored and read back as the same one
"""


def test():
    """
    Store a universally unique identifier, and read it back
    """
    # support
    import uuid

    # access the package
    import pyre.db

    # a table of things with identities
    class Token(pyre.db.table, id="pyre_uuid"):
        """
        Things with identities
        """

        # the key
        id = pyre.db.int().primary()
        # the identity
        identity = pyre.db.uuid()

    # connect
    db = pyre.db.postgres(name="identities").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Token)
        # ask what the column holds
        kind = db.execute(
            "SELECT data_type FROM information_schema.columns"
            " WHERE table_name = 'pyre_uuid' AND column_name = 'identity'"
        )[0][0]
        # it must be an identifier
        assert kind == "uuid", kind
        # pick one
        identity = uuid.UUID("12345678-1234-5678-1234-567812345678")
        # store it
        db.insert(Token.pyre_immutable(id=1, identity=identity))
        # and read it back
        (row,) = db.select(Token)
        # it is the same identifier
        assert row.identity == identity, row.identity
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
