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
    import pyre.records

    class item(pyre.records.record):
        """
        A sample record
        """

        sku = pyre.records.measure()
        description = pyre.records.measure()

    class production(pyre.records.record):
        cost = pyre.records.measure()
        overhead = pyre.records.measure()

    class pricing(item, production):
        price = pyre.records.measure()

    # explore the item record
    assert isinstance(item.sku, pyre.records.measure)
    assert isinstance(item.description, pyre.records.measure)

    assert identical(item.pyre_localFields, (item.sku, item.description))
    assert identical(item.pyre_fields, (item.sku, item.description))
    assert identical(item.pyre_measures, item.pyre_fields)
    assert identical(item.pyre_derivations, ())

    assert item.pyre_columns[item.sku] == 0
    assert item.pyre_columns[item.description] == 1

    # explore the production record
    assert isinstance(production.cost, pyre.records.measure)
    assert isinstance(production.overhead, pyre.records.measure)

    assert identical(production.pyre_localFields, (production.cost, production.overhead))
    assert identical(production.pyre_fields, (production.cost, production.overhead))
    assert identical(production.pyre_measures, (production.cost, production.overhead))
    assert identical(production.pyre_derivations, ())

    assert production.pyre_columns[production.cost] == 0
    assert production.pyre_columns[production.overhead] == 1

    # explore the derived class
    assert isinstance(pricing.sku, pyre.records.measure)
    assert isinstance(pricing.description, pyre.records.measure)
    assert isinstance(pricing.cost, pyre.records.measure)
    assert isinstance(pricing.overhead, pyre.records.measure)
    assert isinstance(pricing.price, pyre.records.measure)

    assert identical(pricing.pyre_localFields, (pricing.price,))
    assert identical(
        pricing.pyre_fields,
        (
            pricing.cost,
            pricing.overhead,
            pricing.sku,
            pricing.description,
            pricing.price,
        ),
    )
    assert identical(pricing.pyre_measures, pricing.pyre_fields)
    assert identical(pricing.pyre_derivations, ())

    assert pricing.pyre_columns[pricing.cost] == 0
    assert pricing.pyre_columns[pricing.overhead] == 1
    assert pricing.pyre_columns[pricing.sku] == 2
    assert pricing.pyre_columns[pricing.description] == 3
    assert pricing.pyre_columns[pricing.price] == 4

    return item, production, pricing


def identical(s1, s2):
    """
    Verify that {s1} and {s2} hold the same nodes, in the same order, and as many of them; the
    nodes are compared by identity, since their {__eq__} builds expressions
    """
    # realize both of them
    s1 = tuple(s1)
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
    # do...
    test()


# end of file
