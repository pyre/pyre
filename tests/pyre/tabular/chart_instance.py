#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Instantiate a simple chart
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
    # make a chart instance
    c = chart()
    # adjust the binning strategy
    
    # and return the chart object
    return c


# main
if __name__ == "__main__":
    test()


# end of file 
