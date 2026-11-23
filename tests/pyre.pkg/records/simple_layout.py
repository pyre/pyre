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
    """
    Declare a record of five measures, and check its fields and their columns
    """
    # access the package
    import pyre.records

    # a record of five measures
    class record(pyre.records.record):
        """
        A sample record
        """

        # the stock keeping unit
        sku = pyre.records.measure()
        # what the item is
        description = pyre.records.measure()
        # what it costs
        cost = pyre.records.measure()
        # its overhead
        overhead = pyre.records.measure()
        # and what it sells for
        price = pyre.records.measure()

    # the fields, in the order of their declaration
    fields = (record.sku, record.description, record.cost, record.overhead, record.price)
    # are all measures
    assert all(isinstance(field, pyre.records.measure) for field in fields)
    # declared locally
    assert record.pyre_localFields == fields
    # which makes them all the fields of the record
    assert identical(record.pyre_fields, record.pyre_localFields)
    # all of its measures
    assert identical(record.pyre_measures, record.pyre_localFields)
    # and leaves it without derivations
    assert identical(record.pyre_derivations, ())
    # each field sits in the column of its position
    assert [record.pyre_columns[field] for field in fields] == [0, 1, 2, 3, 4]

    # all done
    return record


def identical(s1, s2):
    """
    Verify that {s1} and {s2} hold the same nodes, in the same order, and as many of them; the
    nodes are compared by identity, since their {__eq__} builds expressions
    """
    # realize both of them: the first
    s1 = tuple(s1)
    # and the second
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
    # run the test
    test()


# end of file
