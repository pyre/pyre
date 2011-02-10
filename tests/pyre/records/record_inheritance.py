#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify record building in the presence of inheritance
"""


import pyre.records


class item(pyre.records.record):
    """
    A sample record
    """
    sku = pyre.records.field()
    description = pyre.records.field()


class pricing(item):
    cost = pyre.records.field()
    overhead = pyre.records.field()
    price = pyre.records.field()


def test():
    # explore the base
    assert isinstance(item.sku, pyre.records.field)
    assert isinstance(item.description, pyre.records.field)

    assert item.pyre_localItems == (item.sku, item.description)
    assert item.pyre_items == (item.sku, item.description)
    assert item.pyre_fields == (item.sku, item.description)
    assert item.pyre_derivations == ()

    assert item.pyre_index[item.sku] == 0
    assert item.pyre_index[item.description] == 1

    # explore the derived class
    assert isinstance(pricing.sku, pyre.records.field)
    assert isinstance(pricing.description, pyre.records.field)
    assert isinstance(pricing.cost, pyre.records.field)
    assert isinstance(pricing.overhead, pyre.records.field)
    assert isinstance(pricing.price, pyre.records.field)

    assert pricing.pyre_localItems == (pricing.cost, pricing.overhead, pricing.price)
    assert pricing.pyre_items == (
        pricing.sku, pricing.description,
        pricing.cost, pricing.overhead, pricing.price, 
        )
    assert pricing.pyre_fields == pricing.pyre_items
    assert pricing.pyre_derivations == ()

    assert pricing.pyre_index[pricing.sku] == 0
    assert pricing.pyre_index[pricing.description] == 1
    assert pricing.pyre_index[pricing.cost] == 2
    assert pricing.pyre_index[pricing.overhead] == 3
    assert pricing.pyre_index[pricing.price] == 4

    return item, pricing


# main
if __name__ == "__main__":
    test()


# end of file 
