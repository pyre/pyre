#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Detect a change that gives two mutable rows the same primary key
"""


def test():
    """
    Change the primary key of a row of a mutable sheet to the key of another row, and check that
    the next lookup is refused until the conflict is resolved
    """
    # get the package
    import pyre.tabular

    # and its exceptions
    from pyre.tabular.exceptions import DuplicateKeyError

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

    # give the second row the key of the first
    sheet[1].sku = "4000"
    # attempt to
    try:
        # look up the key
        sheet.sku["4000"]
        # which should be refused
        assert False, "unreachable"
    # by saying the key is repeated
    except DuplicateKeyError as error:
        # check that the exception names the key
        assert error.key == "4000"

    # resolve the conflict
    sheet[1].sku = "4002"
    # and check that the first key leads to its row again
    assert sheet.sku["4000"].cost == 2.0
    # and the new one to the other
    assert sheet.sku["4002"].cost == 4.0

    # all done
    return sheet


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
