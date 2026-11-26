#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Add blank rows to a sheet with a primary key, and give them their keys afterwards
"""


def test():
    """
    Add two blank rows to a sheet with a primary key, whose keys are unset and so do not clash,
    then set their keys and check that each leads to its row
    """
    # get the package
    import pyre.tabular

    # a sheet
    class pricing(pyre.tabular.sheet):
        """
        The cost of a few items
        """

        # the stock keeping unit, which identifies the item
        sku = pyre.tabular.str().primary()
        # and the cost
        cost = pyre.tabular.float()

    # make a sheet
    sheet = pricing(name="vegetables")
    # add a blank row
    first = sheet.pyre_new()
    # and another
    second = sheet.pyre_new()
    # check that both made it
    assert len(sheet) == 2

    # give the first its key
    first.sku = "4000"
    # and the second its own
    second.sku = "4001"
    # check that the first key leads to its row
    assert sheet.sku["4000"] is first
    # and so does the second
    assert sheet.sku["4001"] is second

    # all done
    return sheet


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
