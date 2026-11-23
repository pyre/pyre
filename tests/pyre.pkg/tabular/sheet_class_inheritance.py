#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Build a table hierarchy with single inheritance
"""


def test():
    import pyre.tabular

    class raw(pyre.tabular.sheet):
        """
        The sheet layout
        """

        sku = pyre.tabular.measure()
        production = pyre.tabular.measure()
        shipping = pyre.tabular.measure()
        margin = pyre.tabular.measure()
        overhead = pyre.tabular.measure()
        discount = pyre.tabular.measure()

    class pricing(raw):

        cost = raw.production + raw.shipping
        msrp = (1 + raw.margin + raw.overhead) * cost
        price = msrp * (1 - raw.discount)

    # check the base
    assert raw.pyre_name == "raw"
    assert identical(
        raw.pyre_localFields,
        (raw.sku, raw.production, raw.shipping, raw.margin, raw.overhead, raw.discount),
    )
    assert identical(raw.pyre_fields, raw.pyre_localFields)
    assert identical(
        raw.pyre_measures,
        (raw.sku, raw.production, raw.shipping, raw.margin, raw.overhead, raw.discount),
    )
    assert raw.pyre_derivations == ()

    # check the subclass
    assert pricing.pyre_name == "pricing"

    assert identical(pricing.pyre_localFields, (pricing.cost, pricing.msrp, pricing.price))
    assert identical(
        pricing.pyre_fields,
        (
            pricing.sku,
            pricing.production,
            pricing.shipping,
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
            pricing.sku,
            pricing.production,
            pricing.shipping,
            pricing.margin,
            pricing.overhead,
            pricing.discount,
        ),
    )
    assert identical(pricing.pyre_derivations, (pricing.cost, pricing.msrp, pricing.price))

    return pricing, raw


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
