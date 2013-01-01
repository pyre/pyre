#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Build a rudimentary table
"""


def test():
    import pyre.records


    class record(pyre.records.record):
        """
        A sample record
        """
        sku = pyre.records.field()
        description = pyre.records.field()
        cost = pyre.records.field()
        overhead = pyre.records.field()
        price = pyre.records.field()


    # explore the record class
    assert isinstance(record.sku, pyre.records.field)
    assert isinstance(record.description, pyre.records.field)
    assert isinstance(record.cost, pyre.records.field)
    assert isinstance(record.overhead, pyre.records.field)
    assert isinstance(record.price, pyre.records.field)

    assert record.pyre_localEntries == (
        record.sku, record.description, record.cost, record.overhead, record.price)


    assert identical(record.pyre_entries, record.pyre_localEntries)
    assert identical(record.pyre_fields, record.pyre_localEntries)
    assert identical(record.pyre_derivations, ())

    assert record.pyre_index[record.sku] == 0
    assert record.pyre_index[record.description] == 1
    assert record.pyre_index[record.cost] == 2
    assert record.pyre_index[record.overhead] == 3
    assert record.pyre_index[record.price] == 4

    return record


def identical(s1, s2):
    """
    Verify that the nodes in {s1} and {s2} are identical. This has to be done carefully since
    we must avoid triggering __eq__
    """
    for n1, n2 in zip(s1, s2):
        if n1 is not n2: return False
    return True
            

# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
