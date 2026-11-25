#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Refuse to build a simple mutable record from too many values
"""


def test():
    """
    Build a simple mutable record from a row with more values than it has measures, and check
    that the row is refused
    """
    # access the package
    import pyre.records

    # and its exceptions
    from pyre.records.exceptions import RowLengthError

    # a record
    class record(pyre.records.record):
        """
        A sample record
        """

        # the stock keeping unit
        sku = pyre.records.measure()
        # and the cost
        cost = pyre.records.measure()

    # attempt to
    try:
        # build a record from a row with more values than it has measures
        record.pyre_mutable(data=("9-4013", 1.0, 2.0))
        # which should be refused
        assert False, "unreachable"
    # by saying something is wrong with the row
    except RowLengthError:
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
