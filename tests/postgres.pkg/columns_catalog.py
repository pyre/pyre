#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the server records each column with the type the dialect of postgres declares for it
"""


def test():
    """
    Make a table with a column of each type postgres knows, and read their types from the catalog
    """
    # access the package
    import pyre.db

    # a table with a column of each type
    class Columns(pyre.db.table, id="pyre_columns_catalog"):
        """
        A column of each type
        """

        # truth values
        flag = pyre.db.bool(default=None)
        # integers
        count = pyre.db.int(default=None)
        # floating point numbers
        ratio = pyre.db.float(default=None)
        # fixed point numbers
        price = pyre.db.decimal(precision=6, scale=2, default=None)
        # text of bounded length
        state = pyre.db.str(maxlen=2, default=None)
        # and of unbounded length
        name = pyre.db.str(default=None)
        # strings of octets
        payload = pyre.db.bytes(default=None)
        # dates
        day = pyre.db.date(default=None)
        # times of day, without their offsets
        hour = pyre.db.time(default=None)
        # and with them
        local = pyre.db.time(timezone=True, default=None)
        # moments, without their time zones
        moment = pyre.db.timestamp(default=None)
        # and with them
        instant = pyre.db.timestamp(timezone=True, default=None)
        # identifiers
        tag = pyre.db.uuid(default=None)
        # arrays of rank one
        row = pyre.db.array(schema=pyre.db.int(), default=None)
        # of rank two
        grid = pyre.db.array(schema=pyre.db.int(), rank=2, default=None)
        # and of text
        names = pyre.db.array(schema=pyre.db.str(), default=None)
        # documents, in the binary form postgres prefers
        doc = pyre.db.json()
        # and kept as they were written
        raw = pyre.db.json().verbatim()

    # the type the server must record for each column, as its catalog spells it; it keeps the type
    # of the entries of an array, but not its rank
    expected = {
        "flag": "boolean",
        "count": "integer",
        "ratio": "double precision",
        "price": "numeric(6,2)",
        "state": "character varying(2)",
        "name": "text",
        "payload": "bytea",
        "day": "date",
        "hour": "time without time zone",
        "local": "time with time zone",
        "moment": "timestamp without time zone",
        "instant": "timestamp with time zone",
        "tag": "uuid",
        "row": "integer[]",
        "grid": "integer[]",
        "names": "text[]",
        "doc": "jsonb",
        "raw": "json",
    }

    # the exception that ends the block, which takes the table with it
    class Stop(Exception):
        """
        Exception raised to end the transaction block
        """

    # connect
    db = pyre.db.postgres(name="columns_catalog").attach()
    # the types the server recorded
    recorded = None
    # carefully
    try:
        # in a transaction block
        with db:
            # make the table
            db.createTable(Columns)
            # read the type of each of its columns from the catalog
            recorded = {
                name: kind
                for name, kind in db.execute(
                    "SELECT attname, format_type(atttypid, atttypmod) FROM pg_attribute"
                    " WHERE attrelid = 'pyre_columns_catalog'::regclass"
                    " AND attnum > 0 AND NOT attisdropped"
                )
            }
            # and end the block, which rolls back the making of the table
            raise Stop()
    # the end of the block
    except Stop:
        # leaves nothing behind
        pass
    # every column has the type it was meant to have
    assert recorded == expected, {
        name: (recorded.get(name), kind)
        for name, kind in expected.items()
        if recorded.get(name) != kind
    }
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
