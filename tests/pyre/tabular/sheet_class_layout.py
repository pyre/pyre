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

    assert pricing.pyre_localItems == (
        pricing.sku, pricing.production, pricing.shipping, pricing.margin,
        pricing.overhead, pricing.discount,
        pricing.cost, pricing.msrp, pricing.price,
        )
    assert pricing.pyre_items == pricing.pyre_localItems
    assert pricing.pyre_measures == (
        pricing.sku, pricing.production, pricing.shipping, pricing.margin,
        pricing.overhead, pricing.discount,
        )
    assert pricing.pyre_derivations == (
        pricing.cost, pricing.msrp, pricing.price,
        )

    return pricing


# main
if __name__ == "__main__":
    test()


# end of file 
