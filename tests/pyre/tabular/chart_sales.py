#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Read in a couple of tables and build a rudimentary chart
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
    cube.project(transactions)
    # check that the skus were classified correctly
    assert tuple(cube.sku.bins) == ("4000", "4001", "4002", "4003", "4004", "4005")

    # and return the charts and the sheets
    return cube, transactions


# main
if __name__ == "__main__":
    test()


# end of file 
