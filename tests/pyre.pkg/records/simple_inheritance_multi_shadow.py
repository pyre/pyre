#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify which field wins when two bases of a record declare fields by the same name
"""


def test():
    """
    Derive a record from two bases that declare a field by the same name, and check that the
    declaration nearest the derived record in its mro wins, in the slot where the name first
    appeared
    """
    # access the package
    import pyre.records

    # the common ancestor
    class item(pyre.records.record):
        """
        The stock keeping unit of an item
        """

        # the stock keeping unit
        sku = pyre.records.str()

    # one base, which knows the cost as a number
    class production(item):
        """
        What making an item takes
        """

        # the cost
        cost = pyre.records.float()
        # and the overhead
        overhead = pyre.records.float()

    # another base, which knows the cost as text
    class catalog(item):
        """
        How the catalog describes an item
        """

        # the cost, as printed
        cost = pyre.records.str()
        # and the description
        description = pyre.records.str()

    # a record derived from both, which looks for its fields in {production} before {catalog}
    class pricing(production, catalog):
        """
        The prices of the items
        """

        # what the item sells for
        price = pyre.records.float()

    # the cost of the derived record is the one of the base nearest to it
    assert pricing.cost is production.cost
    # and it sits where the name first appeared, among the fields of {catalog}
    assert identical(
        pricing.pyre_fields,
        (item.sku, production.cost, catalog.description, production.overhead, pricing.price),
    )
    # each field sits in the column of its position
    assert [pricing.pyre_columns[field] for field in pricing.pyre_fields] == [0, 1, 2, 3, 4]

    # all done
    return item, production, catalog, pricing


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
