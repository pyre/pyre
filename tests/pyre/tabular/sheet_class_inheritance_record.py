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


class production(pyre.tabular.sheet):

    sku = pyre.tabular.measure()
    production = pyre.tabular.measure()


class shipping(pyre.tabular.sheet):

    shipping = pyre.tabular.measure()


class pricing(production, shipping):

    margin = pyre.tabular.measure()
    overhead = pyre.tabular.measure()
    discount = pyre.tabular.measure()

    cost = production.production + shipping.shipping
    msrp = (1 + margin + overhead)*cost
    price = msrp*(1 - discount)


def test():

    # check production
    record = production.pyre_Record
    # verify the accessors
    assert isinstance(record.sku, pyre.tabular.measure)
    assert isinstance(record.production, pyre.tabular.measure)
    # and their indices
    assert record.pyre_index[record.sku] == 0
    assert record.pyre_index[record.production] == 1

    # check shipping
    record = shipping.pyre_Record
    # verify the accessors
    assert isinstance(record.shipping, pyre.tabular.measure)
    # and their indices
    assert record.pyre_index[record.shipping] == 0

    # and now pricing
    record = pricing.pyre_Record
    # verify the accessors
    assert isinstance(record.margin, pyre.tabular.measure)
    assert isinstance(record.overhead, pyre.tabular.measure)
    assert isinstance(record.discount, pyre.tabular.measure)
    assert isinstance(record.shipping, pyre.tabular.measure)
    assert isinstance(record.sku, pyre.tabular.measure)
    assert isinstance(record.production, pyre.tabular.measure)
    assert isinstance(record.cost, pyre.tabular.derivation)
    assert isinstance(record.msrp, pyre.tabular.derivation)
    assert isinstance(record.price, pyre.tabular.derivation)
    # and their indices
    assert record.pyre_index[record.margin] == 0
    assert record.pyre_index[record.overhead] == 1
    assert record.pyre_index[record.discount] == 2
    assert record.pyre_index[record.sku] == 3
    assert record.pyre_index[record.production] == 4
    assert record.pyre_index[record.shipping] == 5
    assert record.pyre_index[record.cost] == 6
    assert record.pyre_index[record.msrp] == 7
    assert record.pyre_index[record.price] == 8

    return pricing, shipping, production


# main
if __name__ == "__main__":
    test()


# end of file 
