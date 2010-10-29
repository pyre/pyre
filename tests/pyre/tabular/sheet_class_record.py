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
    # access the embedded record object
    record = pricing.pyre_Record
    # verify pedigree
    assert issubclass(record, tuple)
    assert issubclass(record, pyre.tabular.record)
    # verify the accessors
    assert isinstance(record.sku, pyre.tabular.measure)
    assert isinstance(record.production, pyre.tabular.measure)
    assert isinstance(record.shipping, pyre.tabular.measure)
    assert isinstance(record.margin, pyre.tabular.measure)
    assert isinstance(record.overhead, pyre.tabular.measure)
    assert isinstance(record.discount, pyre.tabular.measure)
    assert isinstance(record.cost, pyre.tabular.derivation)
    assert isinstance(record.msrp, pyre.tabular.derivation)
    assert isinstance(record.price, pyre.tabular.derivation)
    # and their indices
    assert record.pyre_index[record.sku] == 0
    assert record.pyre_index[record.production] == 1
    assert record.pyre_index[record.shipping] == 2
    assert record.pyre_index[record.margin] == 3
    assert record.pyre_index[record.overhead] == 4
    assert record.pyre_index[record.discount] == 5
    assert record.pyre_index[record.cost] == 6
    assert record.pyre_index[record.msrp] == 7
    assert record.pyre_index[record.price] == 8

    return pricing


# main
if __name__ == "__main__":
    test()


# end of file 
