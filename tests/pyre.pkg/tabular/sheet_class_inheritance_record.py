#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the class record in the presence of multiple inheritance
"""


def test():
    """
    Derive a sheet from two others, and check the fields of all three and their columns
    """
    # get the package
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

        # measures: the margin
        margin = pyre.tabular.measure()
        # the overhead
        overhead = pyre.tabular.measure()
        # and the discount
        discount = pyre.tabular.measure()
        # derivations: the total cost
        cost = production.production + shipping.shipping
        # the suggested retail price
        msrp = (1 + margin + overhead) * cost
        # and the price after the discount
        price = msrp * (1 - discount)

    # short names for the structural parts: the measures
    measure = pyre.tabular.measure
    # and the derivations
    derivation = pyre.tabular.derivation

    # the first base is a record
    assert issubclass(production, pyre.tabular.record)
    # whose fields
    fields = (production.sku, production.production)
    # are measures
    assert all(isinstance(field, measure) for field in fields)
    # each in the column of its position
    assert [production.pyre_columns[field] for field in fields] == [0, 1]

    # the second base is a record
    assert issubclass(shipping, pyre.tabular.record)
    # whose field is a measure
    assert isinstance(shipping.shipping, measure)
    # in the first column
    assert shipping.pyre_columns[shipping.shipping] == 0

    # the derived sheet is a record
    assert issubclass(pricing, pyre.tabular.record)
    # whose measures, those of the last base first
    measures = (
        pricing.shipping,
        pricing.sku,
        pricing.production,
        pricing.margin,
        pricing.overhead,
        pricing.discount,
    )
    # are measures
    assert all(isinstance(field, measure) for field in measures)
    # and whose derivations
    derivations = (pricing.cost, pricing.msrp, pricing.price)
    # are derivations
    assert all(isinstance(field, derivation) for field in derivations)
    # and each field sits in the column of its position
    assert [pricing.pyre_columns[field] for field in measures + derivations] == list(range(9))

    # all done
    return pricing, shipping, production


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
