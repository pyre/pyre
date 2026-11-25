#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a field redeclared by a derived record shadows the inherited one
"""


def test():
    """
    Derive a record that redeclares one of the fields of its base, and check that the new field
    takes the place of the inherited one, in its slot
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

    # the base record is left alone
    assert identical(item.pyre_fields, (item.sku, item.description))
    # with its stock keeping unit still a number
    assert isinstance(item.sku, pyre.records.int)

    # the derived record declares one field locally
    assert identical(named.pyre_localFields, (named.sku,))
    # which is not the inherited one
    assert named.sku is not item.sku
    # and takes its place, ahead of the field it did not redeclare
    assert identical(named.pyre_fields, (named.sku, item.description))
    # which makes them all measures
    assert identical(named.pyre_measures, named.pyre_fields)
    # each field sits in the column of its position
    assert [named.pyre_columns[field] for field in named.pyre_fields] == [0, 1]

    # the instances have one slot per field
    record = named.pyre_immutable(data=("4000", "tomatoes"))
    # so there are as many values as there are fields
    assert tuple(record) == ("4000", "tomatoes")
    # and the name of the redeclared field reaches the value it converted
    assert record.sku == "4000"

    # all done
    return item, named


def identical(s1, s2):
    """
    Verify that {s1} and {s2} hold the same nodes, in the same order, and as many of them; the
    nodes are compared by identity, since their {__eq__} builds expressions
    """
    # realize both of them: the first
    s1 = tuple(s1)
    # and the second
    s2 = tuple(s2)
    # sequences of different lengths are not identical
    if len(s1) != len(s2):
        # so say so
        return False
    # otherwise, compare the nodes pair by pair
    for n1, n2 in zip(s1, s2):
        # and at the first pair that differs
        if n1 is not n2:
            # say so
            return False
    # all pairs match
    return True


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
