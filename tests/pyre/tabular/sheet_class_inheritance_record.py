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


class production(pyre.tabular.sheet):

    sku = pyre.tabular.auto()
    production = pyre.tabular.auto()


class shipping(pyre.tabular.sheet):

    shipping = pyre.tabular.auto()


class pricing(production, shipping):

    margin = pyre.tabular.auto()
    overhead = pyre.tabular.auto()
    discount = pyre.tabular.auto()

    cost = production.production + shipping.shipping
    msrp = (1 + margin + overhead)*cost
    price = msrp*(1 - discount)


def test():

    # check production
    record = production.pyre_Record
    # verify the accessors
    assert isinstance(record.sku, pyre.tabular.accessor)
    assert isinstance(record.production, pyre.tabular.accessor)
    # and their indices
    assert record.sku.index == 0
    assert record.production.index == 1

    # check shipping
    record = shipping.pyre_Record
    # verify the accessors
    assert isinstance(record.shipping, pyre.tabular.accessor)
    # and their indices
    assert record.shipping.index == 0

    # and now pricing
    record = pricing.pyre_Record
    # verify the accessors
    assert isinstance(record.margin, pyre.tabular.accessor)
    assert isinstance(record.overhead, pyre.tabular.accessor)
    assert isinstance(record.discount, pyre.tabular.accessor)
    assert isinstance(record.cost, pyre.tabular.accessor)
    assert isinstance(record.msrp, pyre.tabular.accessor)
    assert isinstance(record.price, pyre.tabular.accessor)
    assert isinstance(record.shipping, pyre.tabular.accessor)
    assert isinstance(record.sku, pyre.tabular.accessor)
    assert isinstance(record.production, pyre.tabular.accessor)
    # and their indices
    assert record.margin.index == 0
    assert record.overhead.index == 1
    assert record.discount.index == 2
    assert record.cost.index == 3
    assert record.msrp.index == 4
    assert record.price.index == 5
    assert record.sku.index == 6
    assert record.production.index == 7
    assert record.shipping.index == 8

    return pricing, shipping, production


# main
if __name__ == "__main__":
    test()


# end of file 
