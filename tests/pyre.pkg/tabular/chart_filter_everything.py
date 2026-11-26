#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Filter the facts of a chart without any criteria
"""


def test():
    """
    Ask a chart for the facts that satisfy no criteria at all, and check that it selects every
    row of its sheet
    """
    # get the package
    import pyre.tabular

    # a sheet
    class sales(pyre.tabular.sheet):
        """
        The transaction data
        """

        # the date of the sale
        date = pyre.tabular.str()
        # the item sold
        sku = pyre.tabular.str()
        # and the amount
        sale = pyre.tabular.float()

    # a chart
    class chart(pyre.tabular.chart, sheet=sales):
        """
        Categorize the sales by item and date
        """

        # by item
        sku = pyre.tabular.inferred(sales.sku)
        # and by date
        date = pyre.tabular.inferred(sales.date)

    # the data
    data = [
        ("2010/11/01", "4000", 24.24),
        ("2010/11/01", "4005", 2.95),
        ("2010/11/02", "4000", 12.12),
    ]
    # make a sheet
    transactions = sales(name="sales").pyre_immutable(data)
    # and chart it
    cube = chart(sheet=transactions)

    # select the facts that satisfy no criteria
    selection = cube.pyre_filter()
    # and check that they are all the rows of the sheet
    assert selection == {0, 1, 2}, selection

    # all done
    return cube


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
