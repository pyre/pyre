#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the derivations of a base read the fields that shadow their operands
"""


def test():
    """
    Derive a record that redeclares an operand of a derivation of its base, and check that the
    immutable instances compute the derivation from the redeclared field
    """
    # access the package
    import pyre.records

    # the base record
    class item(pyre.records.record):
        """
        An item whose price is its cost plus its overhead
        """

        # the cost, in whole units
        cost = pyre.records.int()
        # the overhead
        overhead = pyre.records.float()
        # and the price
        price = cost + overhead

    # a record that knows its cost in fractions of a unit
    class fine(item):
        """
        An item whose cost need not be whole
        """

        # the cost
        cost = pyre.records.float()

    # build a record with a cost that is not whole
    record = fine.pyre_immutable(data=("1.5", "2"))
    # the cost is converted by the redeclared field
    assert record.cost == 1.5
    # and the price of the base is computed from it
    assert record.price == 3.5
    # and nothing else is in the record
    assert tuple(record) == (1.5, 2.0, 3.5)

    # all done
    return record


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
