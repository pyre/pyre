#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a measure may shadow an inherited derivation
"""


def test():
    """
    Derive a record that redeclares a derivation of its base as a measure, and check that its
    immutable instances take a value for it
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

    # a record whose price is set by hand
    class listed(item):
        """
        An item whose price is given
        """

        # the price
        price = pyre.records.float()

    # the record has no derivations left
    assert listed.pyre_derivations == ()
    # and three measures
    assert len(listed.pyre_measures) == 3

    # build a record whose price is not the sum of the other two
    record = listed.pyre_immutable(data=("1.0", "0.5", "2.0"))
    # the price is the one given
    assert tuple(record) == (1.0, 0.5, 2.0), tuple(record)

    # all done
    return record


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
