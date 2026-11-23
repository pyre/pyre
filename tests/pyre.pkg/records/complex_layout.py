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
    import pyre.records

    class item(pyre.records.record):
        """
        A sample record
        """

        cost = pyre.records.float()
        price = 1.25 * cost

    # explore the record class
    assert isinstance(item.cost, pyre.records.measure)
    assert isinstance(item.price, pyre.records.derivation)

    assert identical(item.pyre_fields, (item.cost, item.price))
    assert identical(item.pyre_measures, (item.cost,))
    assert identical(item.pyre_derivations, (item.price,))

    assert item.pyre_columns[item.cost] == 0
    assert item.pyre_columns[item.price] == 1

    # now instantiate one
    sample = item.pyre_mutable(cost=1.0)
    # check
    assert sample.cost == 1.0
    assert sample.price == 1.25

    return sample


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
