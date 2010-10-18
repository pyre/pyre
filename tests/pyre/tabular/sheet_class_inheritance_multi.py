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

    # check the bases
    assert production.pyre_name == "production"
    assert production.pyre_localMeasures == [ production.sku, production.production ]
    assert production.pyre_inheritedMeasures == []

    assert shipping.pyre_name == "shipping"
    assert shipping.pyre_localMeasures == [ shipping.shipping ]
    assert shipping.pyre_inheritedMeasures == []
    
    # check the subclass
    assert pricing.pyre_name == "pricing"
    assert pricing.pyre_localMeasures == [
        pricing.margin, pricing.overhead, pricing.discount,
        pricing.cost, pricing.msrp, pricing.price
        ]

    assert pricing.pyre_inheritedMeasures == [
        production.sku, production.production, shipping.shipping ]

    return pricing, shipping, production


# main
if __name__ == "__main__":
    test()


# end of file 
