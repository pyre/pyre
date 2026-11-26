#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Follow a change to the primary key of a mutable row
"""


def test():
    """
    Change the primary key of a row of a mutable sheet, twice, and check that each time the new
    key leads to the row and the old one leads nowhere
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

    # the data
    data = [
        ("4000", 2.0),
        ("4001", 4.0),
    ]
    # make a sheet
    sheet = pricing(name="vegetables")
    # and fill it with mutable rows
    sheet.pyre_mutable(data)

    # get the first row
    row = sheet[0]
    # change its key, twice, with no lookups in between
    row.sku = "5000"
    row.sku = "6000"
    # the latest key leads to the row
    assert sheet.sku["6000"] is row
    # and neither of the earlier ones leads anywhere
    for key in ("4000", "5000"):
        # by attempting
        try:
            # to look it up
            sheet.sku[key]
            # which should fail
            assert False, "unreachable"
        # because the key is no longer in the sheet
        except KeyError:
            # so all is well
            pass

    # change the key again, now that the map was rebuilt
    row.sku = "7000"
    # and check that the change is seen too
    assert sheet.sku["7000"] is row
    # and that the other row is unaffected
    assert sheet.sku["4001"].cost == 4.0

    # all done
    return sheet


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
