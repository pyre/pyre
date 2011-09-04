#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Read a sheet from a csv file
"""


def test():
    import pyre.tabular

    class pricing(pyre.tabular.sheet):
        """
        The sheet layout
        """

        # layout
        sku = pyre.tabular.measure()
        description = pyre.tabular.measure()
        production = pyre.tabular.measure()
        overhead = pyre.tabular.measure()
        shipping = pyre.tabular.measure()
        margin = pyre.tabular.measure()
        # type information
        production.type = pyre.schema.float
        overhead.type = pyre.schema.float
        shipping.type = pyre.schema.float
        margin.type = pyre.schema.float


    # make a csv reader
    csv = pyre.tabular.csv()
    # make a sheet
    sheet = pricing(name="vegetables")
    # populate the table
    csv.read(sheet=sheet, uri="vegetables.csv")
    # check that we read the data correctly
    # here is what we expect
    target = [
        ("4000", "tomatoes", 2.95, 5, .2, 50),
        ("4001", "peppers", 0.35, 15, .1, 25),
        ("4002", "grapes", 1.65, 15, .15, 15),
        ("4003", "kiwis", 0.95, 7, .15, 75),
        ("4004", "lemons", 0.50, 4, .25, 50),
        ("4005", "oranges", 0.50, 4, .25, 50),
        ]
    # compare with what we extracted
    for expected, loaded in zip(target, sheet):
        assert expected == tuple(loaded)
    # and return the sheet
    return sheet


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
