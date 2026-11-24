#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that postgres accepts the literals its dialect writes for the values of a row
"""


def test():
    """
    Insert a row with a value of each type, and read back what postgres stored
    """
    # support
    import datetime
    import decimal
    import uuid

    # access the package
    import pyre.db

    # a table with a column of each type
    class Things(pyre.db.table, id="pyre_values"):
        # truth values
        flag = pyre.db.bool()
        # integers
        count = pyre.db.int()
        # floating point numbers
        ratio = pyre.db.float()
        # fixed point numbers
        price = pyre.db.decimal(precision=4, scale=2)
        # text, with a quote in it
        name = pyre.db.str(maxlen=16)
        # strings of octets
        payload = pyre.db.bytes()
        # dates
        day = pyre.db.date()
        # times of day
        hour = pyre.db.time()
        # moments
        moment = pyre.db.timestamp()
        # identifiers
        tag = pyre.db.uuid()
        # arrays
        row = pyre.db.array(schema=pyre.db.int())
        # and one that is left without a value
        missing = pyre.db.str(maxlen=16)

    # a row with a value for each column but the last
    thing = Things.pyre_immutable(
        flag=True,
        count=7,
        ratio=0.5,
        price=decimal.Decimal("12.50"),
        name="O'Hara",
        payload=b"\x00\xff",
        day=datetime.date(2026, 11, 22),
        hour=datetime.time(8, 30),
        moment=datetime.datetime(2026, 11, 22, 8, 30),
        tag=uuid.UUID("12345678-1234-5678-1234-567812345678"),
        row=(1, 2),
    )

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
        "missing",
    )
    # the query that reads them
    query = f"SELECT {', '.join(f'{column}::text' for column in columns)} FROM pyre_values"

    # connect
    db = pyre.db.postgres(name="values").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Things)
        # insert the row
        db.insert(thing)
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
                None,
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
