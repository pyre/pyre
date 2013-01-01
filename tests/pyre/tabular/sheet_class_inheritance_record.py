#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Verify the class record in the presence of multiple inheritance
"""


def test():
    import pyre.tabular
    # save the entry types
    measure = pyre.tabular.measure
    from pyre.records.Derivation import Derivation as derivation

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


    # check production
    record = production.pyre_Record
    # verify the accessors
    assert isinstance(record.sku, pyre.tabular.measure)
    assert isinstance(record.production, pyre.tabular.measure)
    # and their indices
    assert record.pyre_index[record.sku] == 0
    assert record.pyre_index[record.production] == 1

    # check shipping
    record = shipping.pyre_Record
    # verify the accessors
    assert isinstance(record.shipping, pyre.tabular.measure)
    # and their indices
    assert record.pyre_index[record.shipping] == 0

    # and now pricing
    record = pricing.pyre_Record
    # verify the accessors
    assert isinstance(record.margin, measure)
    assert isinstance(record.overhead, measure)
    assert isinstance(record.discount, measure)
    assert isinstance(record.shipping, measure)
    assert isinstance(record.sku, measure)
    assert isinstance(record.production, measure)
    assert isinstance(record.cost, derivation)
    assert isinstance(record.msrp, derivation)
    assert isinstance(record.price, derivation)
    # and their indices
    assert record.pyre_index[record.shipping] == 0
    assert record.pyre_index[record.sku] == 1
    assert record.pyre_index[record.production] == 2
    assert record.pyre_index[record.margin] == 3
    assert record.pyre_index[record.overhead] == 4
    assert record.pyre_index[record.discount] == 5
    assert record.pyre_index[record.cost] == 6
    assert record.pyre_index[record.msrp] == 7
    assert record.pyre_index[record.price] == 8

    return pricing, shipping, production


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
