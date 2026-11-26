#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Refuse a row whose primary key is in the sheet already
"""


def test():
    """
    Fill a sheet with two rows that hold the same primary key, and check that the second one is
    refused with an exception that names the key, the column and the sheet
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

    # the data, with a repeated key
    data = [
        ("4000", 2.0),
        ("4000", 4.0),
    ]
    # make a sheet
    sheet = pricing(name="vegetables")

    # attempt to
    try:
        # fill it
        sheet.pyre_immutable(data)
        # which should be refused
        assert False, "unreachable"
    # by saying the key is repeated
    except DuplicateKeyError as error:
        # check that the exception names the key
        assert error.key == "4000"
        # the column
        assert error.field == "sku"
        # and the sheet
        assert error.name == "vegetables"
        # and that its description says so
        expected = "key '4000' is in more than one row of column 'sku' of 'vegetables'"
        # in so many words
        assert str(error) == expected, str(error)

    # check that the sheet kept the first row only
    assert len(sheet) == 1
    # and that its key still leads to it
    assert sheet.sku["4000"].cost == 2.0

    # all done
    return sheet


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
