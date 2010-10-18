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


class raw(pyre.tabular.sheet):
    """
    The sheet layout
    """

    sku = pyre.tabular.auto()
    production = pyre.tabular.auto()
    shipping = pyre.tabular.auto()
    margin = pyre.tabular.auto()
    overhead = pyre.tabular.auto()
    discount = pyre.tabular.auto()


class pricing(raw):

    cost = raw.production + raw.shipping
    msrp = (1 + raw.margin + raw.overhead)*cost
    price = msrp*(1 - raw.discount)


def test():

    # check the base
    assert raw.pyre_name == "raw"
    assert raw.pyre_localMeasures == [
        raw.sku, raw.production, raw.shipping, raw.margin,
        raw.overhead, raw.discount]
    assert raw.pyre_inheritedMeasures == []

    
    # check the subclass
    assert pricing.pyre_name == "pricing"
    assert pricing.pyre_localMeasures == [
        pricing.cost, pricing.msrp, pricing.price
        ]

    assert pricing.pyre_inheritedMeasures == [
        pricing.sku, pricing.production, pricing.shipping, pricing.margin,
        pricing.overhead, pricing.discount]

    return pricing, raw


# main
if __name__ == "__main__":
    test()


# end of file 
