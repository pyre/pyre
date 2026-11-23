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
    Derive a record with a derivation from three others, check all four, and build an instance
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
        What making an item costs
        """

        # the cost
        cost = pyre.records.measure()

    # a third
    class handling(pyre.records.record):
        """
        What selling an item adds to its cost
        """

        # the overhead, in percent
        overhead = pyre.records.measure()
        # and the margin, in percent
        margin = pyre.records.measure()

    # and a record derived from all three
    class pricing(item, production, handling):
        """
        The prices of the items
        """

        # what the item sells for, computed from its cost, overhead and margin
        price = production.cost * (1 + handling.overhead / 100 + handling.margin / 100)

    # the fields of the first base
    fields = (item.sku, item.description)
    # are measures
    assert all(isinstance(field, pyre.records.measure) for field in fields)
    # declared locally
    assert identical(item.pyre_localFields, fields)
    # which makes them all of its fields
    assert identical(item.pyre_fields, fields)
    # all of its measures
    assert identical(item.pyre_measures, fields)
    # and leaves it without derivations
    assert identical(item.pyre_derivations, ())
    # each field sits in the column of its position
    assert [item.pyre_columns[field] for field in fields] == [0, 1]

    # the field of the second base
    fields = (production.cost,)
    # is a measure
    assert isinstance(production.cost, pyre.records.measure)
    # declared locally
    assert identical(production.pyre_localFields, fields)
    # which makes it its only field
    assert identical(production.pyre_fields, fields)
    # and its only measure
    assert identical(production.pyre_measures, fields)
    # with no derivations
    assert identical(production.pyre_derivations, ())
    # it sits in the first column
    assert production.pyre_columns[production.cost] == 0

    # the fields of the third base
    fields = (handling.overhead, handling.margin)
    # are measures
    assert all(isinstance(field, pyre.records.measure) for field in fields)
    # declared locally
    assert identical(handling.pyre_localFields, fields)
    # which makes them all of its fields
    assert identical(handling.pyre_fields, fields)
    # all of its measures
    assert identical(handling.pyre_measures, fields)
    # and leaves it without derivations
    assert identical(handling.pyre_derivations, ())
    # each field sits in the column of its position
    assert [handling.pyre_columns[field] for field in fields] == [0, 1]

    # the inherited fields of the derived record, those of the last base first
    measures = (
        pricing.overhead,
        pricing.margin,
        pricing.cost,
        pricing.sku,
        pricing.description,
    )
    # are measures
    assert all(isinstance(field, pyre.records.measure) for field in measures)
    # and its own field is a derivation
    assert isinstance(pricing.price, pyre.records.derivation)
    # the only one declared locally
    assert identical(pricing.pyre_localFields, (pricing.price,))
    # placed after the inherited ones among its fields
    assert identical(pricing.pyre_fields, measures + (pricing.price,))
    # its measures are the inherited fields
    assert identical(pricing.pyre_measures, measures)
    # and its derivations its own
    assert identical(pricing.pyre_derivations, (pricing.price,))
    # each field sits in the column of its position
    assert [pricing.pyre_columns[field] for field in pricing.pyre_fields] == [0, 1, 2, 3, 4, 5]

    # build an instance
    p = pricing.pyre_mutable(sku="4013", description="kiwi", cost=1.0, overhead=20, margin=50)
    # its measures hold the values it was given
    assert (p.sku, p.description, p.cost, p.overhead, p.margin) == ("4013", "kiwi", 1.0, 20, 50)
    # and its price is computed from them
    assert p.price == p.cost * (1.0 + p.overhead / 100 + p.margin / 100)

    # all done
    return p


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
