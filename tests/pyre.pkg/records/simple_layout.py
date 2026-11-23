#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Build a simple record and verify its structure
"""


def test():
    import pyre.records

    class record(pyre.records.record):
        """
        A sample record
        """

        sku = pyre.records.measure()
        description = pyre.records.measure()
        cost = pyre.records.measure()
        overhead = pyre.records.measure()
        price = pyre.records.measure()

    # explore the record class
    assert isinstance(record.sku, pyre.records.measure)
    assert isinstance(record.description, pyre.records.measure)
    assert isinstance(record.cost, pyre.records.measure)
    assert isinstance(record.overhead, pyre.records.measure)
    assert isinstance(record.price, pyre.records.measure)

    assert record.pyre_localFields == (
        record.sku,
        record.description,
        record.cost,
        record.overhead,
        record.price,
    )

    assert identical(record.pyre_fields, record.pyre_localFields)
    assert identical(record.pyre_measures, record.pyre_localFields)
    assert identical(record.pyre_derivations, ())

    assert record.pyre_columns[record.sku] == 0
    assert record.pyre_columns[record.description] == 1
    assert record.pyre_columns[record.cost] == 2
    assert record.pyre_columns[record.overhead] == 3
    assert record.pyre_columns[record.price] == 4

    return record


def identical(s1, s2):
    """
    Verify that {s1} and {s2} hold the same nodes, in the same order, and as many of them; the
    nodes are compared by identity, since their {__eq__} builds expressions
    """
    # realize both of them
    s1 = tuple(s1)
    s2 = tuple(s2)
    # sequences of different lengths are not identical
    if len(s1) != len(s2):
        # so say so
        return False
    # otherwise, compare the nodes pair by pair
    for n1, n2 in zip(s1, s2):
        # and at the first pair that differs
        if n1 is not n2:
            # say so
            return False
    # all pairs match
    return True


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
