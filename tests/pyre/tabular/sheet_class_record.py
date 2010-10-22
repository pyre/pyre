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

    sku = pyre.tabular.auto()
    production = pyre.tabular.auto()
    shipping = pyre.tabular.auto()
    margin = pyre.tabular.auto()
    overhead = pyre.tabular.auto()
    discount = pyre.tabular.auto()

    cost = production + shipping
    msrp = (1 + margin + overhead)*cost

    price = msrp*(1 - discount)


def test():
    # access the embedded record object
    record = pricing.pyre_Record
    # verify pedigree
    assert issubclass(record, tuple)
    assert issubclass(record, pyre.tabular.record)
    # verify the accessors
    assert isinstance(record.sku, pyre.tabular.accessor)
    assert isinstance(record.production, pyre.tabular.accessor)
    assert isinstance(record.shipping, pyre.tabular.accessor)
    assert isinstance(record.margin, pyre.tabular.accessor)
    assert isinstance(record.overhead, pyre.tabular.accessor)
    assert isinstance(record.discount, pyre.tabular.accessor)
    assert isinstance(record.cost, pyre.tabular.accessor)
    assert isinstance(record.msrp, pyre.tabular.accessor)
    # and their indices
    assert record.sku.index == 0
    assert record.production.index == 1
    assert record.shipping.index == 2
    assert record.margin.index == 3
    assert record.overhead.index == 4
    assert record.discount.index == 5
    assert record.cost.index == 6
    assert record.msrp.index == 7

    return pricing


# main
if __name__ == "__main__":
    test()


# end of file 
