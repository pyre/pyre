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
    """
    Derive a sheet from two others, and check the fields of all three
    """
    # access the package
    import pyre.tabular

    # a sheet of what making an item costs
    class production(pyre.tabular.sheet):
        """
        Production costs
        """

        # the stock keeping unit
        sku = pyre.tabular.measure()
        # and the cost of making the item
        production = pyre.tabular.measure()

    # a sheet of what shipping it costs
    class shipping(pyre.tabular.sheet):
        """
        Shipping costs
        """

        # the cost of shipping the item
        shipping = pyre.tabular.measure()

    # and a sheet derived from both
    class pricing(production, shipping):
        """
        The prices of the items
        """

        # the margin
        margin = pyre.tabular.measure()
        # the overhead
        overhead = pyre.tabular.measure()
        # the discount
        discount = pyre.tabular.measure()
        # the total cost
        cost = production.production + shipping.shipping
        # the suggested retail price
        msrp = (1 + margin + overhead) * cost
        # and the price after the discount
        price = msrp * (1 - discount)

    # the first base has its name
    assert production.pyre_name == "production"
    # its fields
    fields = (production.sku, production.production)
    # are declared locally
    assert identical(production.pyre_localFields, fields)
    # which makes them all of its fields
    assert identical(production.pyre_fields, fields)
    # all of its measures
    assert identical(production.pyre_measures, fields)
    # and leaves it without derivations
    assert production.pyre_derivations == ()

    # the second base has its name
    assert shipping.pyre_name == "shipping"
    # its field
    fields = (shipping.shipping,)
    # is declared locally
    assert identical(shipping.pyre_localFields, fields)
    # which makes it its only field
    assert identical(shipping.pyre_fields, fields)
    # and its only measure
    assert identical(shipping.pyre_measures, fields)
    # with no derivations
    assert shipping.pyre_derivations == ()

    # the derived sheet has its name
    assert pricing.pyre_name == "pricing"
    # its own fields
    local = (
        pricing.margin,
        pricing.overhead,
        pricing.discount,
        pricing.cost,
        pricing.msrp,
        pricing.price,
    )
    # are declared locally
    assert identical(pricing.pyre_localFields, local)
    # its measures, those of the last base first
    measures = (
        pricing.shipping,
        pricing.sku,
        pricing.production,
        pricing.margin,
        pricing.overhead,
        pricing.discount,
    )
    # and its derivations
    derivations = (pricing.cost, pricing.msrp, pricing.price)
    # make up its fields
    assert identical(pricing.pyre_fields, measures + derivations)
    # sorted into its measures
    assert identical(pricing.pyre_measures, measures)
    # and its derivations
    assert identical(pricing.pyre_derivations, derivations)

    # all done
    return pricing, shipping, production


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
