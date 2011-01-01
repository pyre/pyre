#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
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
    # index on skus
    sku.index = True
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
        ("4001", "peppers", 0.35, 15, .1, 25),
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

    # get the list of skus in the data set ad check it against the dataset
    assert tuple(p.sku) == tuple(record[0] for record in data)
    # compute the average production cost and check we got it right
    assert pyre.patterns.average(p.production) == sum(entry[2] for entry in data)/len(data)
        
    # and return the data set
    return p


# main
if __name__ == "__main__":
    test()


# end of file 
