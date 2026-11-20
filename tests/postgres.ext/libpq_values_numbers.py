#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that numbers reach python as numbers of the matching kind
"""


def test():
    """
    Read a value of each numeric type through the bindings
    """
    # support
    import decimal

    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # ask for one of each
    row = connection.exec(
        "SELECT 7::int2 AS small, 7::int4 AS regular, 9876543210::int8 AS big,"
        " 1.5::float4 AS single, 1.5::float8 AS double, 1.25::numeric(5,2) AS exact"
    )[0]
    # the small whole number is an integer
    assert row["small"] == 7 and type(row["small"]) is int, repr(row["small"])
    # and so is the regular one
    assert row["regular"] == 7 and type(row["regular"]) is int, repr(row["regular"])
    # and the large one
    assert row["big"] == 9876543210 and type(row["big"]) is int, repr(row["big"])
    # the single precision real number is a float
    assert row["single"] == 1.5 and type(row["single"]) is float, repr(row["single"])
    # and so is the double precision one
    assert row["double"] == 1.5 and type(row["double"]) is float, repr(row["double"])
    # the exact number has the right value
    assert row["exact"] == decimal.Decimal("1.25"), repr(row["exact"])
    # and is a decimal, which keeps its scale
    assert type(row["exact"]) is decimal.Decimal, repr(row["exact"])
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
