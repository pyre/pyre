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


import pyre.records


class record(pyre.records.dynamicrecord):
    """
    A sample dynamic record
    """
    cost = pyre.records.field()
    overhead = pyre.records.field()
    price = 1.25*(cost + overhead/100)


def test():
    # explore the record class
    assert isinstance(record.cost, pyre.records.field)
    assert isinstance(record.overhead, pyre.records.field)
    assert isinstance(record.price, pyre.records.derivation)

    assert record.pyre_localItems == (record.cost, record.overhead, record.price)
    assert record.pyre_items == (record.cost, record.overhead, record.price)
    assert record.pyre_fields == (record.cost, record.overhead)
    assert record.pyre_derivations == (record.price,)

    assert record.pyre_index[record.cost] == 0
    assert record.pyre_index[record.overhead] == 1
    assert record.pyre_index[record.price] == 2

    return record


# main
if __name__ == "__main__":
    test()


# end of file 
