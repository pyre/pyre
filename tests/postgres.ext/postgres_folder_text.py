#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a folder server writes the rows of a table in the very text postgres writes for them
when it copies them out, arrays included
"""


def test():
    """
    Put the same rows in postgres and in a folder, copy them out of postgres, and compare the lines
    """
    # externals
    import datetime
    import decimal
    import shutil
    import uuid

    # access the package
    import pyre.db

    # a table with a column of every type the folder writes, and arrays of some of them
    class Reading(pyre.db.table, id="pyre_folder_text"):
        """
        Readings
        """

        # the key
        id = pyre.db.int().primary()
        # a label
        label = pyre.db.str()
        # whether it is good
        good = pyre.db.bool()
        # a measurement
        size = pyre.db.float()
        # a price
        cost = pyre.db.decimal(precision=7, scale=2)
        # a day
        day = pyre.db.date()
        # a time of day
        clock = pyre.db.time()
        # a moment
        moment = pyre.db.timestamp()
        # some octets
        blob = pyre.db.bytes()
        # an identifier
        tag = pyre.db.uuid()
        # the cells of a grid
        cells = pyre.db.array(schema=pyre.db.int(), rank=2)
        # some labels
        labels = pyre.db.array(schema=pyre.db.str())
        # some moments
        moments = pyre.db.array(schema=pyre.db.timestamp())
        # and some flags
        flags = pyre.db.array(schema=pyre.db.bool())

    # the readings
    readings = [
        Reading.pyre_immutable(
            id=1,
            label="a\tb\\c\nd",
            good=True,
            size=1.5,
            cost=decimal.Decimal("2.50"),
            day=datetime.date(2026, 11, 24),
            clock=datetime.time(1, 2, 3),
            moment=datetime.datetime(2026, 11, 24, 1, 2, 3),
            blob=b"\x01\xff",
            tag=uuid.UUID("12345678-1234-5678-1234-567812345678"),
            cells=((1, 2), (3, None)),
            labels=("plain", "a b", "c,d", 'say "hi"', "back\\slash", "", "NULL", "{x}", None),
            moments=(datetime.datetime(2026, 11, 24, 1, 2, 3), None),
            flags=(True, False),
        ),
        Reading.pyre_immutable(id=2, labels=(), cells=()),
    ]

    # the folder, named after this driver and kept for inspection
    folder = "postgres_folder_text"
    # starts out missing
    shutil.rmtree(folder, ignore_errors=True)
    # attach a server to it
    disk = pyre.db.folder(name="folder_text_disk", path=folder).attach()
    # make the table
    disk.createTable(Reading)
    # and put the readings in it
    disk.load(*readings)
    # read its lines
    with open(f"{folder}/pyre_folder_text.tsv") as stream:
        # all of them
        written = stream.read().splitlines()

    # connect
    db = pyre.db.postgres(name="folder_text").attach()
    # make the table
    db.createTable(Reading)
    # carefully
    try:
        # put the readings in it
        db.load(*readings)
        # and copy them out, in the order of their keys
        copied = [
            line.rstrip("\n")
            for line in db.connection.copyOut(
                "COPY (SELECT * FROM pyre_folder_text ORDER BY id) TO STDOUT"
            )
        ]
        # the lines are the same
        assert written == copied, (written, copied)
    # either way
    finally:
        # leave nothing behind
        db.dropTable(Reading)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
