#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the class record structure
"""


def test():
    """
    Declare a sheet with measures and derivations, and check its fields and their columns
    """
    # get the package
    import pyre.tabular

    # the sheet
    class pricing(pyre.tabular.sheet):
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

        # the total cost
        cost = production + shipping
        # the suggested retail price
        msrp = (1 + margin + overhead) * cost
        # and the price after the discount
        price = msrp * (1 - discount)

    # short names for the structural parts: the measures
    measure = pyre.tabular.measure
    # and the derivations
    derivation = pyre.tabular.derivation

    # access the record object
    record = pricing
    # verify pedigree
    assert issubclass(record, pyre.tabular.record)
    # the measures
    measures = (
        record.sku,
        record.production,
        record.shipping,
        record.margin,
        record.overhead,
        record.discount,
    )
    # are measures
    assert all(isinstance(field, measure) for field in measures)
    # the derivations
    derivations = (record.cost, record.msrp, record.price)
    # are derivations
    assert all(isinstance(field, derivation) for field in derivations)
    # and each field sits in the column of its position
    assert [record.pyre_columns[field] for field in measures + derivations] == list(range(9))

    # all done
    return pricing


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
