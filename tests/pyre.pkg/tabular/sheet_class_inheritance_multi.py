#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Build a hierarchy of tables with multiple inheritance
"""


def test():
    import pyre.tabular

    class production(pyre.tabular.sheet):

        sku = pyre.tabular.measure()
        production = pyre.tabular.measure()

    class shipping(pyre.tabular.sheet):

        shipping = pyre.tabular.measure()

    class pricing(production, shipping):

        margin = pyre.tabular.measure()
        overhead = pyre.tabular.measure()
        discount = pyre.tabular.measure()

        cost = production.production + shipping.shipping
        msrp = (1 + margin + overhead) * cost
        price = msrp * (1 - discount)

    # check the bases
    assert production.pyre_name == "production"
    assert identical(production.pyre_localFields, (production.sku, production.production))
    assert identical(production.pyre_fields, (production.sku, production.production))
    assert identical(production.pyre_measures, (production.sku, production.production))
    assert production.pyre_derivations == ()

    assert shipping.pyre_name == "shipping"
    assert identical(shipping.pyre_localFields, (shipping.shipping,))
    assert identical(shipping.pyre_fields, (shipping.shipping,))
    assert identical(shipping.pyre_measures, (shipping.shipping,))
    assert shipping.pyre_derivations == ()

    # check the subclass
    assert pricing.pyre_name == "pricing"
    assert identical(
        pricing.pyre_localFields,
        (
            pricing.margin,
            pricing.overhead,
            pricing.discount,
            pricing.cost,
            pricing.msrp,
            pricing.price,
        ),
    )
    assert identical(
        pricing.pyre_fields,
        (
            pricing.shipping,
            pricing.sku,
            pricing.production,
            pricing.margin,
            pricing.overhead,
            pricing.discount,
            pricing.cost,
            pricing.msrp,
            pricing.price,
        ),
    )
    assert identical(
        pricing.pyre_measures,
        (
            pricing.shipping,
            pricing.sku,
            pricing.production,
            pricing.margin,
            pricing.overhead,
            pricing.discount,
        ),
    )
    assert identical(pricing.pyre_derivations, (pricing.cost, pricing.msrp, pricing.price))

    return pricing, shipping, production


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
