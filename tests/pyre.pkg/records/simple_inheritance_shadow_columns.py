#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a shadowed field finds the column of the field that shadows it
"""


def test():
    """
    Derive a record that redeclares a field of its base, and check that the base's field leads
    to the column of the redeclared one
    """
    # access the package
    import pyre.records

    # the base record
    class item(pyre.records.record):
        """
        A sample record
        """

        # the stock keeping unit, as a number
        sku = pyre.records.int()
        # and what the item is
        description = pyre.records.str()

    # a record that knows its stock keeping units by name
    class named(item):
        """
        A record that redeclares one of the fields of its base
        """

        # the stock keeping unit, as a string
        sku = pyre.records.str()

    # the redeclared field sits in the first column
    assert named.pyre_columns[named.sku] == 0
    # and code that holds the field of the base finds it there
    assert named.pyre_columns[item.sku] == 0
    # while the field that was not redeclared keeps its own
    assert named.pyre_columns[item.description] == 1

    # all done
    return item, named


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
