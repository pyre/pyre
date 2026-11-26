#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Look up the column number of a field of a sheet by its name
"""


def test():
    """
    Ask a sheet for the column of each of its fields, measures and derivations alike, and check
    that each one is the position of the field in the layout
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
        # the price
        price = cost * 2
        # and the markup
        margin = pyre.tabular.float()

    # the names of the fields, in the order of the layout
    names = ("sku", "cost", "price", "margin")
    # check that each one leads to its column
    assert [pricing.pyre_offset(name) for name in names] == [0, 1, 2, 3]

    # all done
    return pricing


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
