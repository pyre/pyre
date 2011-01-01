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


import pyre.records


class item(pyre.records.record):
    """
    A sample record
    """
    cost = pyre.records.field()
    cost.type = pyre.schema.float

    price = 1.25 * cost


def test():
    # explore the record class
    assert isinstance(item.cost, pyre.records.field)
    assert isinstance(item.price, pyre.records.derivation)

    assert item.pyre_localFields == (item.cost,)
    assert item.pyre_inheritedFields == ()
    assert item.pyre_localDerivations == (item.price,)
    assert item.pyre_inheritedDerivations == ()

    assert item.pyre_index[item.cost] == 0
    assert item.pyre_index[item.price] == 1

    # now instantiate one
    sample = item(cost=1.0)
    # check
    assert sample.cost == 1.0
    assert sample.price == 1.25
    
    return sample


# main
if __name__ == "__main__":
    test()


# end of file 
