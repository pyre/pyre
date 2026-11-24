#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a folder server writes the rows of a table in the text format of postgres's copies: a
line for each row, its values in the order the table declares its columns, separated by tabs,
with the characters that would break the line escaped by a backslash, and null as \\N
"""


def test():
    """
    Load two readings of every type into a folder, and check the lines of its file
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
        # a moment
        moment = pyre.db.timestamp()
        # some octets
        blob = pyre.db.bytes()
        # a document
        document = pyre.db.json()
        # and an identifier
        tag = pyre.db.uuid()

    # the folder, named after this driver and kept for inspection
    folder = "folder_load_text"
    # starts out missing
    shutil.rmtree(folder, ignore_errors=True)
    # attach a server to it
    db = pyre.db.folder(name="folder_load_text", path=folder).attach()
    # make the table
    db.createTable(Reading)
    # load a reading with a value in every column
    db.load(
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
            document={"a": 1},
            tag=uuid.UUID("12345678-1234-5678-1234-567812345678"),
        ),
        # and one with an infinity, a falsehood, and nothing else
        Reading.pyre_immutable(id=2, good=False, size=float("-inf")),
    )
    # read the file
    with open(f"{folder}/readings.tsv") as stream:
        # all of it
        text = stream.read()
    # the lines it must hold
    expected = (
        "1\ta\\tb\\\\c\\nd\tt\t1.5\t2.50\t2026-11-24\t01:02:03\t2026-11-24 01:02:03\t"
        '\\\\x01ff\t{"a": 1}\t12345678-1234-5678-1234-567812345678\n'
        "2\t\\N\tf\t-Infinity\t\\N\t\\N\t\\N\t\\N\t\\N\t\\N\t\\N\n"
    )
    # check
    assert text == expected, text
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
