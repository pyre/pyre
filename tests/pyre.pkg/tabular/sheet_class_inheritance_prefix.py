#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A derived sheet starts with the layout of its base, derivations included
"""


def test():
    """
    Derive a sheet that adds a measure to a base that ends in a derivation, and check that the
    fields of the base keep their columns, so a row of the derived sheet reads correctly through
    the columns of the base
    """
    # get the package
    import pyre.tabular

    # the base sheet
    class pricing(pyre.tabular.sheet):
        """
        The cost and markup of a few items, and the price they imply
        """

        # the cost
        cost = pyre.tabular.float()
        # the markup
        margin = pyre.tabular.float()
        # and the price they imply
        price = cost * (1 + margin)

    # a sheet derived from it
    class sales(pricing):
        """
        The prices, along with the discount offered on each item
        """

        # the discount
        discount = pyre.tabular.float()

    # the fields of the base
    fields = (pricing.cost, pricing.margin, pricing.price)
    # lead the fields of the derived sheet
    assert identical(sales.pyre_fields[: len(fields)], fields)
    # and keep their columns there
    assert [sales.pyre_columns[field] for field in fields] == [0, 1, 2]
    # so the new measure comes after them
    assert sales.pyre_columns[sales.discount] == 3

    # make a derived sheet
    sheet = sales(name="vegetables")
    # and fill it
    sheet.pyre_immutable([(2.0, 0.5, 0.1)])
    # get its row
    row = sheet[0]
    # read through the columns of the base, the row holds its cost
    assert row[pricing.pyre_columns[pricing.cost]] == 2.0
    # and its price
    assert row[pricing.pyre_columns[pricing.price]] == 3.0

    # all done
    return sheet


def identical(s1, s2):
    """
    Verify that {s1} and {s2} hold the same nodes, in the same order, and as many of them; the
    nodes are compared by identity, since their {__eq__} builds expressions
    """
    # realize both of them: the first
    s1 = tuple(s1)
    # and the second
    s2 = tuple(s2)
    # they must have the same length
    if len(s1) != len(s2):
        # or they are not identical
        return False
    # and the same nodes in the same places
    return all(n1 is n2 for n1, n2 in zip(s1, s2))


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
