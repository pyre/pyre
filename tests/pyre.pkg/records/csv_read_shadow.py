#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Read records whose layout redeclares an inherited field from a csv file
"""


def test():
    """
    Read a csv source through a record that redeclares a field of its base, and check that the
    column fills the slot of the redeclared field once, converted by it
    """
    # access the package
    import pyre.records

    # the base record
    class item(pyre.records.record):
        """
        The stock keeping unit and margin of an item
        """

        # the stock keeping unit, as a number
        sku = pyre.records.int()
        # and the margin
        margin = pyre.records.float()

    # a record that knows its stock keeping units by name
    class named(item):
        """
        A record that redeclares the stock keeping unit as a string
        """

        # the stock keeping unit, as a string
        sku = pyre.records.str()

    # the records in the file
    target = [
        ("4000", 50.0),
        ("4001", 25.0),
        ("4002", 15.0),
        ("4003", 75.0),
        ("4004", 50.0),
        ("4005", 50.0),
    ]

    # make a reader
    csv = pyre.records.csv()
    # and read the file
    loaded = [tuple(record) for record in csv.immutable(layout=named, uri="vegetables.csv")]
    # each record has one value per field, the stock keeping unit as a string
    assert loaded == target, loaded

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
