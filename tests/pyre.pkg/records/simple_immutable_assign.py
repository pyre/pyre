#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Refuse to change a field of an immutable record
"""


def test():
    """
    Assign a value to a field of an immutable record, and check that the change is refused with
    an exception that names the field, and that the record keeps its value
    """
    # access the package
    import pyre.records

    # and its exceptions
    from pyre.records.exceptions import ImmutableFieldError

    # a record
    class item(pyre.records.record):
        """
        The stock keeping unit and cost of an item
        """

        # the stock keeping unit
        sku = pyre.records.str()
        # and the cost
        cost = pyre.records.float()

    # build an immutable instance
    record = item.pyre_immutable(data=("4000", "1.0"))

    # attempt to
    try:
        # change its cost
        record.cost = 2.0
        # which should be refused
        assert False, "unreachable"
    # by saying the field is immutable
    except ImmutableFieldError as error:
        # check that the exception names the field
        assert error.field == "cost"
        # and the record
        assert error.name == "item"
        # and that its description says so
        assert str(error) == "field 'cost' of 'item' is immutable", str(error)

    # check that the record kept its value
    assert record.cost == 1.0

    # all done
    return record


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
