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

    # check the bases
    assert production.pyre_name == "production"
    assert production.pyre_localMeasures == ( production.sku, production.production )
    assert production.pyre_inheritedMeasures == ()
    assert production.pyre_localDerivations == ()
    assert production.pyre_inheritedDerivations == ()

    assert shipping.pyre_name == "shipping"
    assert shipping.pyre_localMeasures == ( shipping.shipping, )
    assert shipping.pyre_inheritedMeasures == ()
    assert shipping.pyre_localDerivations == ()
    assert shipping.pyre_inheritedDerivations == ()
    
    # check the subclass
    assert pricing.pyre_name == "pricing"
    assert pricing.pyre_localMeasures == ( pricing.margin, pricing.overhead, pricing.discount )
    assert pricing.pyre_inheritedMeasures == (
        production.sku, production.production, shipping.shipping )
    assert pricing.pyre_localDerivations == (pricing.cost, pricing.msrp, pricing.price)
    assert pricing.pyre_inheritedDerivations == ()

    return pricing, shipping, production


# main
if __name__ == "__main__":
    test()


# end of file 
