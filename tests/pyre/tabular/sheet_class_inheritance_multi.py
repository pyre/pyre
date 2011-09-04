#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Build a hierarchy of tables with multiple inheritance
"""


def test():
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


    # check the bases
    assert production.pyre_name == "production"
    assert production.pyre_localItems == ( production.sku, production.production )
    assert production.pyre_items == ( production.sku, production.production )
    assert production.pyre_measures == ( production.sku, production.production )
    assert production.pyre_derivations == ()

    assert shipping.pyre_name == "shipping"
    assert shipping.pyre_localItems == ( shipping.shipping, )
    assert shipping.pyre_items == ( shipping.shipping, )
    assert shipping.pyre_measures == ( shipping.shipping, )
    assert shipping.pyre_derivations == ()
    
    # check the subclass
    assert pricing.pyre_name == "pricing"
    assert pricing.pyre_localItems == (
        pricing.margin, pricing.overhead, pricing.discount,
        pricing.cost, pricing.msrp, pricing.price
        )
    assert pricing.pyre_items == (
        pricing.shipping,
        pricing.sku, pricing.production,
        pricing.margin, pricing.overhead, pricing.discount,
        pricing.cost, pricing.msrp, pricing.price
        )
    assert pricing.pyre_measures == (
        pricing.shipping,
        pricing.sku, pricing.production,
        pricing.margin, pricing.overhead, pricing.discount,
        )
    assert pricing.pyre_derivations == (
        pricing.cost, pricing.msrp, pricing.price
        )
    
    return pricing, shipping, production


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
