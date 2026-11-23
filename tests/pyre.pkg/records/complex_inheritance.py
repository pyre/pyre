#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify record building in the presence of inheritance, with a derivation in the derived record
"""


def test():
    """
    Derive a record with a derivation from one of measures, check both, and build an instance
    """
    # access the package
    import pyre.records

    # the base record
    class item(pyre.records.record):
        """
        A sample record
        """

        # the stock keeping unit
        sku = pyre.records.measure()
        # what the item is
        description = pyre.records.measure()
        # and what it costs
        cost = pyre.records.measure()

    # a record derived from it
    class pricing(item):
        """
        The prices of the items
        """

        # what the item sells for, computed from its cost
        price = 2 * item.cost

    # the fields of the base
    fields = (item.sku, item.description, item.cost)
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
    assert [item.pyre_columns[field] for field in fields] == [0, 1, 2]

    # the inherited fields of the derived record
    measures = (pricing.sku, pricing.description, pricing.cost)
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
    assert [pricing.pyre_columns[field] for field in pricing.pyre_fields] == [0, 1, 2, 3]

    # build an instance
    p = pricing.pyre_mutable(sku="4013", description="kiwi", cost=1.0)
    # its measures hold the values it was given
    assert (p.sku, p.description, p.cost) == ("4013", "kiwi", 1.0)
    # and its price is computed from them
    assert p.price == 2 * p.cost

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
