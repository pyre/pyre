#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Create a record that has a derived field
"""


def test():
    import pyre.records

    class item(pyre.records.record):
        """
        A sample record
        """
        production = pyre.records.float()
        shipping = pyre.records.float()
        cost = production + shipping
        price = 2 * cost


    # explore the record class
    assert isinstance(item.production, pyre.records.field)
    assert isinstance(item.shipping, pyre.records.field)
    assert isinstance(item.cost, pyre.records.derivation)
    assert isinstance(item.price, pyre.records.derivation)

    assert item.pyre_items == (item.production, item.shipping, item.cost, item.price)
    assert item.pyre_fields == (item.production, item.shipping)
    assert item.pyre_derivations == (item.cost, item.price)

    assert item.pyre_index[item.production] == 0
    assert item.pyre_index[item.shipping] == 1
    assert item.pyre_index[item.cost] == 2
    assert item.pyre_index[item.price] == 3

    # now instantiate one
    sample = item(production=0.8, shipping=0.2)
    # check
    assert sample.production == 0.8
    assert sample.shipping == 0.2
    assert sample.cost == 1.0
    assert sample.price == 2.0
    
    return sample


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
