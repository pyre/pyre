#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Create a record that has a derived field
"""


def test():
    import pyre.records

    class item(pyre.records.dynamicrecord):
        """
        A sample record
        """
        cost = pyre.records.field()
        cost.type = pyre.schema.float

        price = 1.25 * cost


    # explore the record class
    assert isinstance(item.cost, pyre.records.field)
    assert isinstance(item.price, pyre.records.derivation)

    assert item.pyre_items == (item.cost, item.price)
    assert item.pyre_fields == (item.cost,)
    assert item.pyre_derivations == (item.price,)

    assert item.pyre_index[item.cost] == 0
    assert item.pyre_index[item.price] == 1

    # now instantiate one
    sample = item(cost=1.0)
    # check
    assert sample.cost == 1.0
    assert sample.price == 1.25
    # modify
    sample.cost = 4
    assert sample.cost == 4.0
    assert sample.price == 5.0
    
    return sample


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
