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


class raw(pyre.tabular.sheet):
    """
    The sheet layout
    """

    sku = pyre.tabular.measure()
    production = pyre.tabular.measure()
    shipping = pyre.tabular.measure()
    margin = pyre.tabular.measure()
    overhead = pyre.tabular.measure()
    discount = pyre.tabular.measure()


class pricing(raw):

    cost = raw.production + raw.shipping
    msrp = (1 + raw.margin + raw.overhead)*cost
    price = msrp*(1 - raw.discount)


def test():

    # check the base
    assert raw.pyre_name == "raw"
    assert raw.pyre_localMeasures == (
        raw.sku, raw.production, raw.shipping, raw.margin,
        raw.overhead, raw.discount)
    assert raw.pyre_inheritedMeasures == ()
    assert raw.pyre_localDerivations == ()
    assert raw.pyre_inheritedDerivations == ()

    
    # check the subclass
    assert pricing.pyre_name == "pricing"
    assert pricing.pyre_localMeasures == ()
    assert pricing.pyre_inheritedMeasures == (
        pricing.sku, pricing.production, pricing.shipping, pricing.margin,
        pricing.overhead, pricing.discount )
    assert pricing.pyre_localDerivations == ( pricing.cost, pricing.msrp, pricing.price )
    assert pricing.pyre_inheritedDerivations == ()

    return pricing, raw


# main
if __name__ == "__main__":
    test()


# end of file 
