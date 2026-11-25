#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Refuse to build a complex mutable record from a keyword that names a computed field
"""


def test():
    """
    Build a complex mutable record from keywords, one of which names a computed field,
    and check that it is refused
    """
    # access the package
    import pyre.records

    # and its exceptions
    from pyre.records.exceptions import ComputedFieldError

    # a record
    class record(pyre.records.record):
        """
        A sample record
        """

        # the stock keeping unit
        sku = pyre.records.measure()
        # the cost
        cost = pyre.records.measure()
        # and the price, which depends on the cost
        price = 1.25 * cost + 0.25

    # build a record with a price of its own
    try:
        record.pyre_mutable(sku="9-4013", cost=1.0, price=2.0)
        # which should be refused
        assert False, "unreachable"
    # by saying the price is computed
    except ComputedFieldError:
        # which is what we expect
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
