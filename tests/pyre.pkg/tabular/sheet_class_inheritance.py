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
    """
    Derive a sheet of derivations from one of measures, and check both
    """
    # access the package
    import pyre.tabular

    # the sheet of measures
    class raw(pyre.tabular.sheet):
        """
        The sheet layout
        """

        # the stock keeping unit
        sku = pyre.tabular.measure()
        # the cost of making the item
        production = pyre.tabular.measure()
        # the cost of shipping it
        shipping = pyre.tabular.measure()
        # the margin
        margin = pyre.tabular.measure()
        # the overhead
        overhead = pyre.tabular.measure()
        # and the discount
        discount = pyre.tabular.measure()

    # a sheet derived from it
    class pricing(raw):
        """
        The prices of the items
        """

        # the total cost
        cost = raw.production + raw.shipping
        # the suggested retail price
        msrp = (1 + raw.margin + raw.overhead) * cost
        # and the price after the discount
        price = msrp * (1 - raw.discount)

    # the base has its name
    assert raw.pyre_name == "raw"
    # its measures
    measures = (raw.sku, raw.production, raw.shipping, raw.margin, raw.overhead, raw.discount)
    # are declared locally
    assert identical(raw.pyre_localFields, measures)
    # which makes them all of its fields
    assert identical(raw.pyre_fields, raw.pyre_localFields)
    # all of its measures
    assert identical(raw.pyre_measures, measures)
    # and leaves it without derivations
    assert raw.pyre_derivations == ()

    # the derived sheet has its own name
    assert pricing.pyre_name == "pricing"
    # its inherited measures
    measures = (
        pricing.sku,
        pricing.production,
        pricing.shipping,
        pricing.margin,
        pricing.overhead,
        pricing.discount,
    )
    # and its own derivations
    derivations = (pricing.cost, pricing.msrp, pricing.price)
    # which are its local fields
    assert identical(pricing.pyre_localFields, derivations)
    # follow the inherited ones among its fields
    assert identical(pricing.pyre_fields, measures + derivations)
    # and are sorted into its measures
    assert identical(pricing.pyre_measures, measures)
    # and its derivations
    assert identical(pricing.pyre_derivations, derivations)

    # all done
    return pricing, raw


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
