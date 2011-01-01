#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that chart class records get built as expected
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
    # check the sheet class
    assert chart.pyre_Sheet == sales
    # check the dimensions
    assert chart.pyre_localDimensions == (chart.sku,)
    assert chart.pyre_inheritedDimensions == ()
    assert chart.pyre_dimensions == (chart.sku,)
    # and return the chart
    return chart


# main
if __name__ == "__main__":
    test()


# end of file 
