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


def test():
    import pyre.calc
    import pyre.tabular
    import pyre.records

    class record(pyre.tabular.record):
        """
        A sample record
        """
        sku = pyre.tabular.measure()
        description = pyre.tabular.measure()
        cost = pyre.tabular.measure()
        overhead = pyre.tabular.measure()
        price = cost + overhead


    # explore the record class
    assert isinstance(record.sku, pyre.tabular.measure)
    assert isinstance(record.description, pyre.tabular.measure)
    assert isinstance(record.cost, pyre.tabular.measure)
    assert isinstance(record.overhead, pyre.tabular.measure)
    assert isinstance(record.price, pyre.records.derivation)

    assert record.pyre_index[record.sku] == 0
    assert record.pyre_index[record.description] == 1
    assert record.pyre_index[record.cost] == 2
    assert record.pyre_index[record.overhead] == 3
    assert record.pyre_index[record.price] == 4

    # build a record
    r = record(sku="9-4013", description="organic kiwi", cost=.85, overhead=.15)
    # check
    assert r.sku == "9-4013"
    assert r.description == "organic kiwi"
    assert r.cost == .85
    assert r.overhead == .15
    assert r.price == 1.0
    # set to different values
    r.cost = 1.0 
    # check again
    assert r.cost == 1.0
    assert r.price == 1.15

    return r


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
