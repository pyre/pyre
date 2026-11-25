#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Refuse to read records from a csv source that names two of its columns alike
"""


def test():
    """
    Read a csv source with two columns by the same name, and check that the source is refused
    """
    # externals
    import io

    # access the package
    import pyre.records

    # and its exceptions
    from pyre.records.exceptions import AmbiguousColumnError

    # a record
    class item(pyre.records.record):
        """
        The stock keeping unit and cost of an item
        """

        # the stock keeping unit
        sku = pyre.records.str()
        # and the cost
        cost = pyre.records.float()

    # a source with two columns named {cost}
    source = io.StringIO("sku,cost,cost\n4000,1.0,2.0\n")

    # make a reader
    csv = pyre.records.csv()
    # attempt to
    try:
        # read the source
        tuple(csv.immutable(layout=item, stream=source))
        # which should be refused
        assert False, "unreachable"
    # by saying the source is ambiguous
    except AmbiguousColumnError:
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
