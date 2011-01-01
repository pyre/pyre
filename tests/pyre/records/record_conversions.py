#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise data conversions
"""


import pyre.records


class record(pyre.records.record):
    """
    A sample record
    """
    # field declarations
    sku = pyre.records.field()
    description = pyre.records.field()
    cost = pyre.records.field()
    overhead = pyre.records.field()
    price = pyre.records.field()

    # type information
    sku.type = pyre.schema.str
    description.type = pyre.schema.str
    cost.type = pyre.schema.float
    overhead.type = pyre.schema.float
    price.type = pyre.schema.float


def test():
    # build a record
    r = record(sku="9-4013", description="organic kiwi", cost=".85", overhead=".15", price="1")
    # check
    assert r.sku == "9-4013"
    assert r.description == "organic kiwi"
    assert r.cost == .85
    assert r.overhead == .15
    assert r.price == 1.0

    return r


# main
if __name__ == "__main__":
    test()


# end of file 
