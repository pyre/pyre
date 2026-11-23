#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Build a rudimentary table
"""


def test():
    """
    Declare a sheet with measures and derivations, and check its name and its structure
    """
    # access the package
    import pyre.tabular

    # the sheet
    class pricing(pyre.tabular.sheet):
        """
        The sheet layout
        """

        # measures: the stock keeping unit
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
        # derivations: the total cost
        cost = production + shipping
        # the suggested retail price
        msrp = (1 + margin + overhead) * cost
        # and the price after the discount
        price = msrp * (1 - discount)

    # check the name
    assert pricing.pyre_name == "pricing"

    # the measures
    measures = (
        pricing.sku,
        pricing.production,
        pricing.shipping,
        pricing.margin,
        pricing.overhead,
        pricing.discount,
    )
    # and the derivations
    derivations = (pricing.cost, pricing.msrp, pricing.price)
    # are all declared locally, in order
    assert identical(pricing.pyre_localFields, measures + derivations)
    # which makes them all the fields of the sheet
    assert identical(pricing.pyre_fields, pricing.pyre_localFields)
    # sorted into its measures
    assert identical(pricing.pyre_measures, measures)
    # and its derivations
    assert identical(pricing.pyre_derivations, derivations)

    # all done
    return pricing


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
