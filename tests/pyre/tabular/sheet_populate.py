#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Build a rudimentary table
"""


import pyre.tabular


class pricing(pyre.tabular.sheet):
    """
    The sheet layout
    """
    # layout
    sku = pyre.tabular.measure()
    description = pyre.tabular.measure()
    production = pyre.tabular.measure()
    shipping = pyre.tabular.measure()
    margin = pyre.tabular.measure()
    overhead = pyre.tabular.measure()
    # type information
    sku.type = pyre.schema.str
    description.type = pyre.schema.str
    production.type = pyre.schema.float
    overhead.type = pyre.schema.float
    shipping.type = pyre.schema.float
    margin.type = pyre.schema.float


def test():
    # our data set
    data = [
        ("4000", "tomatoes", 2.95, 5, .2, 50),
        ("4001", "pepers", 0.35, 15, .1, 25),
        ("4002", "grapes", 1.65, 15, .15, 15),
        ("4003", "kiwis", 0.95, 7, .15, 75),
        ("4004", "lemons", 0.50, 4, .25, 50),
        ("4005", "oranges", 0.50, 4, .25, 50),
        ]
    # make a sheet
    p = pricing(name="vegetables")
    # iterate over the data set
    for datum in data:
        # populate the sheet
        p.append(record=p.pyre_Record(datum))
    # check that all is good
    for expected, actual in zip(data, p):
        assert expected == tuple(node.value for node in actual)
        
    # and return the data set
    return p


# main
if __name__ == "__main__":
    test()


# end of file 
