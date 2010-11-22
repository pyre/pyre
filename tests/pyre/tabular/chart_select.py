#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
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
    # here are the skus and dates we expect to retrieve from the data set
    skus = ("4000", "4001", "4002", "4003", "4004", "4005")
    dates = ("2010/11/01","2010/11/02","2010/11/03","2010/11/04","2010/11/05",)
    # check that the skus were classified correctly
    assert tuple(sku for sku, bin in cube.sku.bins) == skus
    # check that the dates were classified correctly
    assert tuple(date for date, bin in cube.date.bins) == dates

    # select the records the match a given sku and date
    grp = cube.pyre_select(sku="4000", date="2010/11/01")

    # and return the charts and the sheets
    return cube, transactions


# main
if __name__ == "__main__":
    test()


# end of file 
