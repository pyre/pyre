#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that postgres stores the values that are not finite as its dialect writes them
"""


def test():
    """
    Insert infinities and values that are not numbers, and read back what postgres stored
    """
    # support
    import decimal

    # access the package
    import pyre.db

    # a table of measurements
    class Measurement(pyre.db.table, id="pyre_nonfinite"):
        # the key
        id = pyre.db.int().primary()
        # a floating point value
        ratio = pyre.db.float()
        # and a fixed point one
        price = pyre.db.decimal(precision=8, scale=2)

    # the rows: infinities, which postgres stores only in floating point columns, since a fixed
    # point column with a precision has no room for them, and values that are not numbers
    rows = [
        Measurement.pyre_immutable(id=1, ratio=float("inf")),
        Measurement.pyre_immutable(id=2, ratio=float("-inf")),
        Measurement.pyre_immutable(id=3, ratio=float("nan"), price=decimal.Decimal("NaN")),
    ]

    # connect
    db = pyre.db.postgres(name="nonfinite").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Measurement)
        # insert the rows
        db.insert(*rows)
        # read back what postgres stored, as text
        stored = [
            tuple(row)
            for row in db.execute("SELECT ratio::text, price::text FROM pyre_nonfinite ORDER BY id")
        ]
        # and check it
        assert stored == [
            ("Infinity", None),
            ("-Infinity", None),
            ("NaN", "NaN"),
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
