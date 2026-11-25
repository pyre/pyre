#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the records a load copies into a table come back with their values, for every type of
column the dialect has
"""


def test():
    """
    Load two records of every type, and read them back
    """
    # support
    import datetime
    import decimal
    import uuid

    # access the package
    import pyre.db

    # a table with a column of every type
    class Sample(pyre.db.table, id="pyre_load"):
        """
        Samples
        """

        # the key
        id = pyre.db.int().primary()
        # text
        name = pyre.db.str()
        # a truth value
        good = pyre.db.bool()
        # a fixed point number
        value = pyre.db.decimal(precision=6, scale=2)
        # a floating point one
        ratio = pyre.db.float()
        # a date
        day = pyre.db.date()
        # a moment, with its offset
        instant = pyre.db.timestamp(timezone=True)
        # an identifier
        tag = pyre.db.uuid()
        # octets
        payload = pyre.db.bytes()
        # a document
        doc = pyre.db.json()
        # and an array
        cells = pyre.db.array(schema=pyre.db.int())

    # the records
    records = [
        Sample.pyre_immutable(
            id=index,
            name=f"sample {index}",
            good=index % 2 == 0,
            value=decimal.Decimal(f"{index}.25"),
            ratio=index / 4,
            day=datetime.date(2026, 11, index),
            instant=datetime.datetime(2026, 11, index, 8, 30, tzinfo=datetime.timezone.utc),
            tag=uuid.UUID(int=index),
            payload=bytes([index, 0, 255]),
            doc={"index": index, "words": ["a", "b"]},
            cells=(index, index + 1),
        )
        for index in range(1, 3)
    ]

    # connect
    db = pyre.db.postgres(name="load").attach()
    # make the table
    db.createTable(Sample)
    # carefully
    try:
        # load the records
        db.load(*records)
        # read them back, in order
        rows = sorted(db.select(Sample), key=lambda row: row.id)
        # they came back with their values
        assert [tuple(row) for row in rows] == [tuple(record) for record in records], rows
    # either way
    finally:
        # leave nothing behind
        db.dropTable(Sample)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
