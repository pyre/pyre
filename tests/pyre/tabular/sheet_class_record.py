#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify the class record structure
"""


def test():
    import pyre.tabular
    # save the entry types
    measure = pyre.tabular.measure
    from pyre.records.Derivation import Derivation as derivation

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


    # access the embedded record object
    record = pricing.pyre_Record
    # verify pedigree
    assert issubclass(record, tuple)
    # verify the accessors
    assert isinstance(record.sku, measure)
    assert isinstance(record.production, measure)
    assert isinstance(record.shipping, measure)
    assert isinstance(record.margin, measure)
    assert isinstance(record.overhead, measure)
    assert isinstance(record.discount, measure)
    assert isinstance(record.cost, derivation)
    assert isinstance(record.msrp, derivation)
    assert isinstance(record.price, derivation)
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
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
