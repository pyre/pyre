#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Refuse to read records from a csv source that lacks the column of a required field
"""


def test():
    """
    Read a csv source without a column for a required field, and check that the source is
    refused with an exception that names the field
    """
    # externals
    import io

    # access the package
    import pyre.records

    # and its exceptions
    from pyre.records.exceptions import MissingColumnError

    # a record
    class item(pyre.records.record):
        """
        The stock keeping unit and cost of an item
        """

        # the stock keeping unit
        sku = pyre.records.str()
        # and the cost
        cost = pyre.records.float()
        # which every item must have
        cost.optional = False

    # a source without a column for the cost
    source = io.StringIO("sku,price\n4000,2.0\n")

    # make a reader
    csv = pyre.records.csv()
    # attempt to
    try:
        # read the source
        tuple(csv.immutable(layout=item, stream=source))
        # which should be refused
        assert False, "unreachable"
    # by saying the source has no column for the cost
    except MissingColumnError as error:
        # check that the exception names the field
        assert error.field == "cost"
        # and the record
        assert error.name == "item"
        # and carries the headers of the source
        assert error.headers == ("sku", "price")
        # and that its description says so
        assert str(error) == "field 'cost' of 'item' matches no column", str(error)

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
