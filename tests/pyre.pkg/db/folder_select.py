#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a folder server reads back the rows it writes, every value in the type of its column
"""


def test():
    """
    Load readings of every type into a folder, select them, and compare
    """
    # externals
    import datetime
    import decimal
    import shutil
    import uuid

    # access the package
    import pyre.db

    # a table with a column of every type the folder writes
    class Reading(pyre.db.table, id="readings"):
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
        # a moment, with its offset from utc
        moment = pyre.db.timestamp()
        # some octets
        blob = pyre.db.bytes()
        # a document
        document = pyre.db.json()
        # and an identifier
        tag = pyre.db.uuid()

    # the values of the readings, by column
    readings = [
        (
            1,
            "a\tb\\c\nd\re",
            True,
            1.5,
            decimal.Decimal("2.50"),
            datetime.date(2026, 11, 24),
            datetime.time(1, 2, 3, 456789),
            datetime.datetime(2026, 11, 24, 1, 2, 3, tzinfo=datetime.timezone.utc),
            b"\x00\x01\xff",
            {"a": [1, 2.5, "three"], "b": None},
            uuid.UUID("12345678-1234-5678-1234-567812345678"),
        ),
        (2, "", False, float("inf"), None, None, None, None, b"", [], None),
        (3, None, None, None, None, None, None, None, None, None, None),
    ]
    # the names of the columns
    names = [field.name for field in Reading.pyre_fields]

    # the folder, named after this driver and kept for inspection
    folder = "folder_select"
    # starts out missing
    shutil.rmtree(folder, ignore_errors=True)
    # attach a server to it
    db = pyre.db.folder(name="folder_select", path=folder).attach()
    # make the table
    db.createTable(Reading)
    # load the readings
    db.load(*(Reading.pyre_immutable(**dict(zip(names, values))) for values in readings))
    # read them back
    selected = [tuple(row) for row in db.select(query=Reading)]
    # they are the ones that went in, in order
    assert selected == readings, selected
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
