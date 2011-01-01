#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
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


class handling(pyre.records.record):
    overhead = pyre.records.field()
    margin = pyre.records.field()


class pricing(item, production, handling):
    price = production.cost * (1 + handling.overhead/100 + handling.margin/100)


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

    assert production.pyre_localFields == (production.cost,)
    assert production.pyre_inheritedFields == ()
    assert tuple(production.pyre_fields()) == (production.cost,)

    assert production.pyre_index[production.cost] == 0

    # explore the overhead record
    assert isinstance(handling.overhead, pyre.records.field)
    assert isinstance(handling.margin, pyre.records.field)

    assert handling.pyre_localFields == (handling.overhead, handling.margin)
    assert handling.pyre_inheritedFields == ()
    assert tuple(handling.pyre_fields()) == (handling.overhead, handling.margin)

    assert handling.pyre_index[handling.overhead] == 0
    assert handling.pyre_index[handling.margin] == 1

    # explore the derived class
    assert isinstance(pricing.sku, pyre.records.field)
    assert isinstance(pricing.description, pyre.records.field)
    assert isinstance(pricing.cost, pyre.records.field)
    assert isinstance(pricing.overhead, pyre.records.field)
    assert isinstance(pricing.margin, pyre.records.field)
    assert isinstance(pricing.price, pyre.records.derivation)

    assert pricing.pyre_localFields == ()
    assert pricing.pyre_inheritedFields == (
        pricing.sku, pricing.description,
        pricing.cost, pricing.overhead, pricing.margin
        )
    assert tuple(pricing.pyre_fields()) == (
        pricing.sku, pricing.description, 
        pricing.cost, pricing.overhead, pricing.margin
        )
    assert pricing.pyre_localDerivations == (pricing.price,)
    assert pricing.pyre_inheritedDerivations == ()

    assert pricing.pyre_index[pricing.sku] == 0
    assert pricing.pyre_index[pricing.description] == 1
    assert pricing.pyre_index[pricing.cost] == 2
    assert pricing.pyre_index[pricing.overhead] == 3
    assert pricing.pyre_index[pricing.margin] == 4
    assert pricing.pyre_index[pricing.price] == 5

    # now instantiate one
    p = pricing(sku="4013", description="kiwi", cost=1.0, overhead=20, margin=50)
    # check
    assert p.sku == "4013"
    assert p.description == "kiwi"
    assert p.cost == 1.0
    assert p.overhead == 20
    assert p.margin == 50
    assert p.price == p.cost*(1.0 + p.overhead/100 + p.margin/100)

    return p


# main
if __name__ == "__main__":
    test()


# end of file 
