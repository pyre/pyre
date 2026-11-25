#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a derivation may shadow an inherited measure
"""


def test():
    """
    Derive a record that redeclares a measure of its base as a derivation, and check that its
    immutable instances take one value fewer, and compute the rest from it
    """
    # access the package
    import pyre.records

    # the base record
    class item(pyre.records.record):
        """
        An item whose price is its cost plus its overhead
        """

        # the cost
        cost = pyre.records.float()
        # the overhead
        overhead = pyre.records.float()
        # and the price
        price = cost + overhead

    # a record whose cost is twice its overhead
    class lean(item):
        """
        An item whose cost follows from its overhead
        """

        # the cost
        cost = 2 * item.overhead

    # the cost of the derived record is a derivation in the slot of the measure
    assert lean.pyre_fields[0] is lean.cost
    # which leaves the overhead as the only measure
    assert len(lean.pyre_measures) == 1 and lean.pyre_measures[0] is item.overhead

    # build a record from its overhead alone
    record = lean.pyre_immutable(data=("1.5",))
    # the cost is computed from the overhead, and the price from both
    assert tuple(record) == (3.0, 1.5, 4.5), tuple(record)

    # all done
    return record


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
