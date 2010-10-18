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

    sku = pyre.tabular.auto()
    production = pyre.tabular.auto()
    shipping = pyre.tabular.auto()
    margin = pyre.tabular.auto()
    overhead = pyre.tabular.auto()
    discount = pyre.tabular.auto()

    cost = production + shipping
    msrp = (1 + margin + overhead)*cost

    price = msrp*(1 - discount)


def test():

    assert pricing.pyre_name == "pricing"

    assert pricing.pyre_localMeasures == [
        pricing.sku, pricing.production, pricing.shipping, pricing.margin,
        pricing.overhead, pricing.discount, pricing.cost, pricing.msrp,
        pricing.price
        ]

    assert pricing.pyre_inheritedMeasures == []

    return pricing


# main
if __name__ == "__main__":
    test()


# end of file 
