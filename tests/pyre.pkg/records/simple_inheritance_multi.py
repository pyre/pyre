#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify record building in the presence of multiple inheritance
"""


def test():
    """
    Derive a record from two others, and check that the derived one places the fields of its
    bases ahead of its own, the last base first
    """
    # access the package
    import pyre.records

    # one base record
    class item(pyre.records.record):
        """
        A sample record
        """

        # the stock keeping unit
        sku = pyre.records.measure()
        # and what the item is
        description = pyre.records.measure()

    # another
    class production(pyre.records.record):
        """
        What making an item takes
        """

        # what the item costs
        cost = pyre.records.measure()
        # and its overhead
        overhead = pyre.records.measure()

    # and a record derived from both
    class pricing(item, production):
        """
        The prices of the items
        """

        # what the item sells for
        price = pyre.records.measure()

    # the fields of the first base
    fields = (item.sku, item.description)
    # are measures
    assert all(isinstance(field, pyre.records.measure) for field in fields)
    # declared locally
    assert identical(item.pyre_localFields, fields)
    # which makes them all of its fields
    assert identical(item.pyre_fields, fields)
    # all of its measures
    assert identical(item.pyre_measures, item.pyre_fields)
    # and leaves it without derivations
    assert identical(item.pyre_derivations, ())
    # each field sits in the column of its position
    assert [item.pyre_columns[field] for field in fields] == [0, 1]

    # the fields of the second base
    fields = (production.cost, production.overhead)
    # are measures
    assert all(isinstance(field, pyre.records.measure) for field in fields)
    # declared locally
    assert identical(production.pyre_localFields, fields)
    # which makes them all of its fields
    assert identical(production.pyre_fields, fields)
    # all of its measures
    assert identical(production.pyre_measures, fields)
    # and leaves it without derivations
    assert identical(production.pyre_derivations, ())
    # each field sits in the column of its position
    assert [production.pyre_columns[field] for field in fields] == [0, 1]

    # the fields of the derived record: those of the last base, then the first, then its own
    fields = (pricing.cost, pricing.overhead, pricing.sku, pricing.description, pricing.price)
    # are measures
    assert all(isinstance(field, pyre.records.measure) for field in fields)
    # one of which is declared locally
    assert identical(pricing.pyre_localFields, (pricing.price,))
    # and all of which are its fields
    assert identical(pricing.pyre_fields, fields)
    # and its measures
    assert identical(pricing.pyre_measures, pricing.pyre_fields)
    # with no derivations
    assert identical(pricing.pyre_derivations, ())
    # each field sits in the column of its position
    assert [pricing.pyre_columns[field] for field in fields] == [0, 1, 2, 3, 4]

    # all done
    return item, production, pricing


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
