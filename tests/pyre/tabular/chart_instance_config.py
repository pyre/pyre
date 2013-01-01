#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Instantiate a simple chart
"""


def test():
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
        quantity = pyre.tabular.interval(measure=sales.quantity, interval=(0, 20), subdivisions=4)


    # make a chart instance
    c = chart()
    # check that the instance picked up the expected dimensions
    assert c._pyre_initialized == False
    assert c.quantity.start == 0
    assert c.quantity.end == 20
    assert c.quantity.subdivisions == 4
    # adjust the binning strategy
    c.quantity.subdivisions = 2
    # check that theconfiguration was updated
    assert c.quantity.subdivisions == 2
    # verify that no bin storage has been allocated yet
    assert c.quantity.intervals == None
    # initialize the chart
    c.pyre_initialize()
    # and check that storage was allocated
    assert c.quantity.intervals == (set(), set())
    
    # and return the chart object
    return c


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
