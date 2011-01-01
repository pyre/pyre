#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise chart interval dimensions
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
    quantity = pyre.tabular.interval(measure=sales.quantity, interval=(0, 20), subdivisions=4)


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
    # there should have been no rejects in this sample dataset
    assert cube.quantity.rejects == set()
    # check that all transactions were binned
    assert len(transactions) == sum(len(bin) for interval, bin in cube.quantity.bins)
    
    # and return the chart object
    return cube


# main
if __name__ == "__main__":
    test()


# end of file 
