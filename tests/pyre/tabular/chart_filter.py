#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise an inferred chart dimension
"""


import pyre.tabular


class sales(pyre.tabular.sheet):
    """The transaction data"""
    # layout
    date = pyre.tabular.str()
    time = pyre.tabular.str()
    sku = pyre.tabular.str()
    quantity = pyre.tabular.float()
    discount = pyre.tabular.float()
    sale = pyre.tabular.float()


class chart(pyre.tabular.chart, sheet=sales):
    """
    Aggregate the information in the {sales} table
    """
    sku = pyre.tabular.inferred(sales.sku)
    date = pyre.tabular.inferred(sales.date)


def test():
    # make a csv reader
    csv = pyre.tabular.csv()
    # make a sheet
    transactions = sales(name="sales")
    # populate the tables
    csv.read(sheet=transactions, uri="sales.csv")
    # build a chart
    cube = chart()
    # bin the transactions
    cube.pyre_project(transactions)

    # select the records the match a given sku and date
    grp = cube.pyre_filter(date="2010/11/01", sku="4000")
    # check that we got what we expected
    assert grp == {0, 5, 6}

    # and return the chart and the sheet
    return cube, transactions


# main
if __name__ == "__main__":
    test()


# end of file 
