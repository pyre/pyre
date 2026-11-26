#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Read the values of a derived column of a sheet
"""


def test():
    """
    Build a sheet with a column derived from two of its measures, and check that the derived
    column yields the value of its expression in every row
    """
    # get the package
    import pyre.tabular

    # a sheet
    class pricing(pyre.tabular.sheet):
        """
        The cost and markup of a few items, and the price they imply
        """

        # the stock keeping unit
        sku = pyre.tabular.str()
        # the cost
        cost = pyre.tabular.float()
        # the markup
        margin = pyre.tabular.float()
        # and the price they imply
        price = cost * (1 + margin)

    # the data
    data = [
        ("4000", 2.0, 0.5),
        ("4001", 4.0, 0.25),
        ("4002", 8.0, 0.125),
    ]
    # make a sheet
    sheet = pricing(name="vegetables")
    # and fill it
    sheet.pyre_immutable(data)

    # the prices we expect
    expected = [3.0, 5.0, 9.0]
    # read the derived column
    prices = list(sheet.price)
    # and check that it holds the price of every row
    assert prices == expected, prices

    # all done
    return sheet


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
