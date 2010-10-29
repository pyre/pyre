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

    sku = pyre.tabular.measure()
    production = pyre.tabular.measure()
    shipping = pyre.tabular.measure()
    margin = pyre.tabular.measure()
    overhead = pyre.tabular.measure()
    discount = pyre.tabular.measure()

    cost = production + shipping
    msrp = (1 + margin + overhead)*cost

    price = msrp*(1 - discount)


def test():

    assert pricing.pyre_name == "pricing"

    assert pricing.pyre_localMeasures == (
        pricing.sku, pricing.production, pricing.shipping, pricing.margin,
        pricing.overhead, pricing.discount
        )
    assert pricing.pyre_inheritedMeasures == ()
    assert pricing.pyre_localDerivations == (pricing.cost, pricing.msrp, pricing.price,)
    assert pricing.pyre_inheritedDerivations == ()

    return pricing


# main
if __name__ == "__main__":
    test()


# end of file 
