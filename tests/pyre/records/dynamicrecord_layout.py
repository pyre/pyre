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
    import pyre.records

    class record(pyre.records.dynamicrecord):
        """
        A sample dynamic record
        """
        cost = pyre.records.field()
        overhead = pyre.records.field()
        price = 1.25*(cost + overhead/100)


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
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
