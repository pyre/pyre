#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a derivation that shadows an inherited measure follows the fields it depends on
"""


def test():
    """
    Derive a record that redeclares a measure of its base as a derivation, and check that its
    mutable instances compute the derivation, and follow changes of the fields it depends on
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

    # build a record from its overhead alone
    record = lean.pyre_mutable(data=("1.5",))
    # the cost is computed from the overhead, and the price from both
    assert (record.cost, record.overhead, record.price) == (3.0, 1.5, 4.5)

    # change the overhead
    record.overhead = 2.0
    # and the cost and the price follow
    assert (record.cost, record.price) == (4.0, 6.0), (record.cost, record.price)

    # all done
    return record


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
