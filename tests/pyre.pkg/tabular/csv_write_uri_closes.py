#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the csv writer closes the file it opens once the records are written
"""


def test():
    """
    Write a sheet to a csv file named by its uri, and check that the writer leaves no file open
    behind it, and that the file holds every record
    """
    # externals
    import gc
    import warnings

    # access the package
    import pyre.tabular

    # lay out a sheet
    class pricing(pyre.tabular.sheet):
        """
        The price of each item
        """

        # the stock keeping unit
        sku = pyre.tabular.str()
        # the description
        description = pyre.tabular.str()
        # and the price
        price = pyre.tabular.float()

    # make a sheet
    sheet = pricing(name="vegetables")
    # and fill it
    sheet.pyre_immutable(data=[("4000", "tomatoes", "2.95"), ("4001", "peppers", "0.35")])

    # make a writer
    csv = pyre.tabular.csv()
    # watch for the warning python issues when it collects a file that is still open
    with warnings.catch_warnings(record=True) as caught:
        # by recording every one of them
        warnings.simplefilter("always", ResourceWarning)
        # write the sheet to a file named after this test
        csv.write(sheet=sheet, uri="csv_write_uri_closes.csv")
        # and collect what is left of the writer
        gc.collect()

    # check that nothing was left open
    leaks = [warning for warning in caught if issubclass(warning.category, ResourceWarning)]
    # by finding no warnings about it
    assert not leaks, [str(leak.message) for leak in leaks]

    # read the file back
    with open("csv_write_uri_closes.csv", newline="") as stream:
        # all of it
        text = stream.read()
    # it should hold a row of headers, and a row for each record
    expected = "".join(
        (
            "sku,description,price\r\n",
            "4000,tomatoes,2.95\r\n",
            "4001,peppers,0.35\r\n",
        )
    )
    # which it does
    assert text == expected, text

    # all done
    return sheet


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
