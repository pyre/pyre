#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Load records from a csv file
"""


def test():
    import pyre.records

    # layout the record
    class item(pyre.records.record):
        # the fields
        sku = pyre.records.str()
        description = pyre.records.str()
        production = pyre.records.float()
        overhead = pyre.records.float()
        shipping = pyre.records.float()
        margin = pyre.records.float()
        # a derived quantity
        price = production * (1 + overhead / 100 + margin / 100) + shipping

    # build the target tuple
    target = [
        ("4000", "tomatoes", 2.95, 5, 0.2, 50, 2.95 * (1 + 0.05 + 0.5) + 0.2),
        ("4001", "peppers", 0.35, 15, 0.1, 25, 0.35 * (1 + 0.15 + 0.25) + 0.1),
        ("4002", "grapes", 1.65, 15, 0.15, 15, 1.65 * (1 + 0.15 + 0.15) + 0.15),
        ("4003", "kiwis", 0.95, 7, 0.15, 75, 0.95 * (1 + 0.07 + 0.75) + 0.15),
        ("4004", "lemons", 0.50, 4, 0.25, 50, 0.5 * (1 + 0.04 + 0.5) + 0.25),
        ("4005", "oranges", 0.50, 4, 0.25, 50, 0.5 * (1 + 0.04 + 0.5) + 0.25),
    ]

    # create the reader
    csv = pyre.records.csv()
    # read the csv data
    source = csv.immutable(layout=item, uri="vegetables.csv")
    # check
    for given, loaded in zip(target, source):
        assert given == loaded

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
