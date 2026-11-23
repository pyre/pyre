#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Create a record that has a derived field
"""


def test():
    """
    Declare a record with a measure and a derivation, check its structure, and build an instance
    """
    # access the package
    import pyre.records

    # a record with a derived field
    class item(pyre.records.record):
        """
        A sample record
        """

        # what the item costs
        cost = pyre.records.float()
        # and what it sells for, computed from its cost
        price = 1.25 * cost

    # the cost is a measure
    assert isinstance(item.cost, pyre.records.measure)
    # and the price a derivation
    assert isinstance(item.price, pyre.records.derivation)
    # the record holds both, in the order of their declaration
    assert identical(item.pyre_fields, (item.cost, item.price))
    # one of which is a measure
    assert identical(item.pyre_measures, (item.cost,))
    # and the other a derivation
    assert identical(item.pyre_derivations, (item.price,))
    # each field sits in the column of its position
    assert [item.pyre_columns[field] for field in (item.cost, item.price)] == [0, 1]

    # build an instance
    sample = item.pyre_mutable(cost=1.0)
    # its cost is the one it was given
    assert sample.cost == 1.0
    # and its price is computed from it
    assert sample.price == 1.25

    # all done
    return sample


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
