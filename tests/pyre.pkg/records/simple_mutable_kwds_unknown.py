#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Refuse to build a simple mutable record from a keyword that names none of its fields
"""


def test():
    """
    Build a simple mutable record from keywords, one of which is misspelled, and check that the
    misspelled one is refused
    """
    # access the package
    import pyre.records

    # and its exceptions
    from pyre.records.exceptions import UnknownFieldError

    # a record
    class record(pyre.records.record):
        """
        A sample record
        """

        # the stock keeping unit
        sku = pyre.records.measure()
        # and the cost
        cost = pyre.records.measure()

    # build a record with a misspelled cost
    try:
        record.pyre_mutable(sku="9-4013", cots=1.0)
        # which should be refused
        assert False, "unreachable"
    # by saying something is wrong with the keywords
    except UnknownFieldError:
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
