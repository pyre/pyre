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

    class handling(pyre.records.record):
        overhead = pyre.records.measure()
        margin = pyre.records.measure()

    class pricing(item, production, handling):
        price = production.cost * (1 + handling.overhead / 100 + handling.margin / 100)

    # explore the item record
    assert isinstance(item.sku, pyre.records.measure)
    assert isinstance(item.description, pyre.records.measure)

    assert identical(item.pyre_localFields, (item.sku, item.description))
    assert identical(item.pyre_fields, (item.sku, item.description))
    assert identical(item.pyre_measures, (item.sku, item.description))
    assert identical(item.pyre_derivations, ())

    assert item.pyre_columns[item.sku] == 0
    assert item.pyre_columns[item.description] == 1

    # explore the production record
    assert isinstance(production.cost, pyre.records.measure)

    assert identical(production.pyre_localFields, (production.cost,))
    assert identical(production.pyre_fields, (production.cost,))
    assert identical(production.pyre_measures, (production.cost,))
    assert identical(production.pyre_derivations, ())

    assert production.pyre_columns[production.cost] == 0

    # explore the handling record
    assert isinstance(handling.overhead, pyre.records.measure)
    assert isinstance(handling.margin, pyre.records.measure)

    assert identical(handling.pyre_localFields, (handling.overhead, handling.margin))
    assert identical(handling.pyre_fields, (handling.overhead, handling.margin))
    assert identical(handling.pyre_measures, (handling.overhead, handling.margin))
    assert identical(handling.pyre_derivations, ())

    assert handling.pyre_columns[handling.overhead] == 0
    assert handling.pyre_columns[handling.margin] == 1

    # explore the derived class
    assert isinstance(pricing.sku, pyre.records.measure)
    assert isinstance(pricing.description, pyre.records.measure)
    assert isinstance(pricing.cost, pyre.records.measure)
    assert isinstance(pricing.overhead, pyre.records.measure)
    assert isinstance(pricing.margin, pyre.records.measure)
    assert isinstance(pricing.price, pyre.records.derivation)

    assert identical(pricing.pyre_localFields, (pricing.price,))
    assert identical(
        pricing.pyre_fields,
        (
            pricing.overhead,
            pricing.margin,
            pricing.cost,
            pricing.sku,
            pricing.description,
            pricing.price,
        ),
    )
    assert identical(
        pricing.pyre_measures,
        (
            pricing.overhead,
            pricing.margin,
            pricing.cost,
            pricing.sku,
            pricing.description,
        ),
    )
    assert identical(pricing.pyre_derivations, (pricing.price,))

    assert pricing.pyre_columns[pricing.overhead] == 0
    assert pricing.pyre_columns[pricing.margin] == 1
    assert pricing.pyre_columns[pricing.cost] == 2
    assert pricing.pyre_columns[pricing.sku] == 3
    assert pricing.pyre_columns[pricing.description] == 4
    assert pricing.pyre_columns[pricing.price] == 5

    # now instantiate one
    cost = 1.0
    overhead = 20
    margin = 50
    p = pricing.pyre_mutable(
        sku="4013", description="kiwi", cost=cost, overhead=overhead, margin=margin
    )
    # check
    assert p.sku == "4013"
    assert p.description == "kiwi"
    assert p.cost == 1.0
    assert p.overhead == 20
    assert p.margin == 50
    assert p.price == p.cost * (1.0 + p.overhead / 100 + p.margin / 100)

    return p


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
