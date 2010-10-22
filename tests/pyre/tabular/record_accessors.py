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


import pyre.calc
import pyre.tabular


class record(pyre.tabular.record):
    """
    A sample record
    """
    sku = pyre.tabular.accessor(index=0)
    description = pyre.tabular.accessor(index=1)
    cost = pyre.tabular.accessor(index=2)
    overhead = pyre.tabular.accessor(index=3)
    price = pyre.tabular.accessor(index=4)

    def __new__(cls, sku, description, cost):
        # build the model nodes
        n_sku = pyre.calc.newNode(value=sku)
        n_description = pyre.calc.newNode(value=description)
        n_cost = pyre.calc.newNode(value=cost)
        n_overhead = pyre.calc.newNode(value=.15)
        n_price = n_cost + n_overhead
        # place them in a tuple
        nodes = (n_sku, n_description, n_cost, n_overhead, n_price)
        # build the record
        return super().__new__(cls, nodes)


def test():
    # explore the record class
    assert isinstance(record.sku, pyre.tabular.accessor)
    assert isinstance(record.description, pyre.tabular.accessor)
    assert isinstance(record.price, pyre.tabular.accessor)

    assert record.sku.index == 0
    assert record.description.index == 1
    assert record.cost.index == 2
    assert record.overhead.index == 3
    assert record.price.index == 4

    # build a record
    r = record(sku="9-4013", description="organic kiwi", cost=.85)
    # check
    assert r.sku == "9-4013"
    assert r.description == "organic kiwi"
    assert r.cost == .85
    assert r.overhead == .15
    assert r.price == 1.0
    # set to different values
    r.cost = 1.0 
    # check again
    assert r.cost == 1.0
    assert r.price == 1.15

    return r


# main
if __name__ == "__main__":
    test()


# end of file 
