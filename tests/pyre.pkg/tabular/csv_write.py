#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Write the records of a sheet to a stream in csv format
"""


def test():
    """
    Write a sheet to a stream, and check that the stream holds a row of headers followed by a
    row for each record, and that it is left open for its owner
    """
    # externals
    import io

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

    # make a stream
    stream = io.StringIO()
    # and a writer
    csv = pyre.tabular.csv()
    # write the sheet to the stream
    csv.write(sheet=sheet, stream=stream)

    # the stream belongs to us, so it is still open
    assert not stream.closed
    # it should hold a row of headers, and a row for each record
    expected = "".join(
        (
            "sku,description,price\r\n",
            "4000,tomatoes,2.95\r\n",
            "4001,peppers,0.35\r\n",
        )
    )
    # which it does
    assert stream.getvalue() == expected, stream.getvalue()

    # all done
    return sheet


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
