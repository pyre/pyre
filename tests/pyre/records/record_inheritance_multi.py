#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify record building in the presence of multiple inheritance
"""


import pyre.records


class item(pyre.records.record):
    """
    A sample record
    """
    sku = pyre.records.field()
    description = pyre.records.field()


class production(pyre.records.record):
    cost = pyre.records.field()
    overhead = pyre.records.field()


class pricing(item, production):
    price = pyre.records.field()


def test():
    # explore the item record
    assert isinstance(item.sku, pyre.records.field)
    assert isinstance(item.description, pyre.records.field)

    assert item.pyre_localFields == (item.sku, item.description)
    assert item.pyre_inheritedFields == ()
    assert tuple(item.pyre_fields()) == (item.sku, item.description)

    assert item.pyre_index[item.sku] == 0
    assert item.pyre_index[item.description] == 1

    # explore the production record
    assert isinstance(production.cost, pyre.records.field)
    assert isinstance(production.overhead, pyre.records.field)

    assert production.pyre_localFields == (production.cost, production.overhead)
    assert production.pyre_inheritedFields == ()
    assert tuple(production.pyre_fields()) == (production.cost, production.overhead)

    assert production.pyre_index[production.cost] == 0
    assert production.pyre_index[production.overhead] == 1

    # explore the derived class
    assert isinstance(pricing.sku, pyre.records.field)
    assert isinstance(pricing.description, pyre.records.field)
    assert isinstance(pricing.cost, pyre.records.field)
    assert isinstance(pricing.overhead, pyre.records.field)
    assert isinstance(pricing.price, pyre.records.field)

    assert pricing.pyre_localFields == (pricing.price,)
    assert pricing.pyre_inheritedFields == (
        pricing.sku, pricing.description,
        pricing.cost, pricing.overhead
        )
    assert tuple(pricing.pyre_fields()) == (
        pricing.price, 
        pricing.sku, pricing.description, 
        pricing.cost, pricing.overhead
        )

    assert pricing.pyre_index[pricing.price] == 0
    assert pricing.pyre_index[pricing.sku] == 1
    assert pricing.pyre_index[pricing.description] == 2
    assert pricing.pyre_index[pricing.cost] == 3
    assert pricing.pyre_index[pricing.overhead] == 4

    return item, pricing


# main
if __name__ == "__main__":
    test()


# end of file 
