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
    sku = pyre.tabular.str()
    sku.index = True

    description = pyre.tabular.str()
    production = pyre.tabular.float()
    shipping = pyre.tabular.float()
    margin = pyre.tabular.float()
    overhead = pyre.tabular.float()

    msrp = (production*(1+margin/100) + shipping)*(1+overhead/100)


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
    # make a sheet out of the data set
    p = pricing(name="vegetables").populate(data)

    # grab the kiwi record
    kiwi = p.sku["4003"]
    # check that the record is correct
    assert abs(kiwi.msrp - 13.92) < .01
    # make small change in the production cost
    kiwi.production = 1.15
    # check that the update is reflected in the msrp f kiwis
    assert abs(kiwi.msrp - 14.26) < .01

    # and return the data set
    return p


# main
if __name__ == "__main__":
    test()


# end of file 
