#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that postgres accepts the defaults its dialect declares, and fills them in
"""


def test():
    """
    Make a table with a default for each column, insert a row that names only its key, and
    read back what postgres stored
    """
    # support
    import datetime
    import decimal
    import uuid

    # access the package
    import pyre.db

    # a table with a column of each type, each with a default
    class Defaults(pyre.db.table, id="pyre_defaults"):
        # the key
        id = pyre.db.int().primary()
        # truth values
        flag = pyre.db.bool(default=True)
        # integers
        count = pyre.db.int(default=7)
        # floating point numbers
        ratio = pyre.db.float(default=0.5)
        # fixed point numbers
        price = pyre.db.decimal(precision=4, scale=2, default=decimal.Decimal("12.50"))
        # text, with a quote in it
        name = pyre.db.str(maxlen=16, default="O'Hara")
        # strings of octets
        payload = pyre.db.bytes(default=b"\x00\xff")
        # dates
        day = pyre.db.date(default=datetime.date(2026, 11, 22))
        # times of day
        hour = pyre.db.time(default=datetime.time(8, 30))
        # moments
        moment = pyre.db.timestamp(default=datetime.datetime(2026, 11, 22, 8, 30))
        # identifiers
        tag = pyre.db.uuid(default=uuid.UUID("12345678-1234-5678-1234-567812345678"))
        # arrays of rank one
        row = pyre.db.array(schema=pyre.db.int(), default=(1, 2))
        # of rank two
        grid = pyre.db.array(schema=pyre.db.int(), rank=2, default=((1, 2), (3, 4)))
        # and empty ones
        empty = pyre.db.array(schema=pyre.db.int(), default=())

    # the columns, read back as the text postgres renders them
    columns = (
        "flag",
        "count",
        "ratio",
        "price",
        "name",
        "payload",
        "day",
        "hour",
        "moment",
        "tag",
        "row",
        "grid",
        "empty",
    )
    # the query that reads them
    query = f"SELECT {', '.join(f'{column}::text' for column in columns)} FROM pyre_defaults"

    # connect
    db = pyre.db.postgres(name="defaults").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Defaults)
        # insert a row that names only its key
        db.execute("INSERT INTO pyre_defaults (id) VALUES (1)")
        # read back what postgres stored
        stored = [tuple(row) for row in db.execute(query)]
        # and check it
        assert stored == [
            (
                "true",
                "7",
                "0.5",
                "12.50",
                "O'Hara",
                "\\x00ff",
                "2026-11-22",
                "08:30:00",
                "2026-11-22 08:30:00",
                "12345678-1234-5678-1234-567812345678",
                "{1,2}",
                "{{1,2},{3,4}}",
                "{}",
            )
        ], stored
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
