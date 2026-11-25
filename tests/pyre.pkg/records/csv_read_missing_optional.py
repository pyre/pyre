#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Read records from a csv file that lacks the column of one of their optional fields
"""


def test():
    """
    Read a csv source that has no column for an optional field, and check that the field takes
    its default while the fields after it get their own columns
    """
    # access the package
    import pyre.records

    # a record with a field the file does not have
    class item(pyre.records.record):
        """
        The stock keeping unit, cost and margin of an item
        """

        # the stock keeping unit
        sku = pyre.records.str()
        # the cost, which is optional
        cost = pyre.records.float()
        cost.optional = True
        cost.default = 1.0
        # and the margin
        margin = pyre.records.float()

    # the records in the file, each with the default cost
    target = [
        ("4000", 1.0, 50.0),
        ("4001", 1.0, 25.0),
        ("4002", 1.0, 15.0),
        ("4003", 1.0, 75.0),
        ("4004", 1.0, 50.0),
        ("4005", 1.0, 50.0),
    ]

    # make a reader
    csv = pyre.records.csv()
    # and read the file
    loaded = [tuple(record) for record in csv.immutable(layout=item, uri="vegetables.csv")]
    # each record has the default cost, and the margin from its own column
    assert loaded == target, loaded

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
