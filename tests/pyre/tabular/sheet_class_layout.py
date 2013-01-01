#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Build a rudimentary table
"""


def test():
    import pyre.tabular

    class pricing(pyre.tabular.sheet):
        """
        The sheet layout
        """

        sku = pyre.tabular.measure()
        production = pyre.tabular.measure()
        shipping = pyre.tabular.measure()
        margin = pyre.tabular.measure()
        overhead = pyre.tabular.measure()
        discount = pyre.tabular.measure()

        cost = production + shipping
        msrp = (1 + margin + overhead)*cost

        price = msrp*(1 - discount)


    assert pricing.pyre_name == "pricing"

    assert identical(pricing.pyre_localEntries, (
        pricing.sku, pricing.production, pricing.shipping, pricing.margin,
        pricing.overhead, pricing.discount,
        pricing.cost, pricing.msrp, pricing.price,
        ))
    assert identical(pricing.pyre_entries, pricing.pyre_localEntries)
    assert identical(pricing.pyre_fields, (
        pricing.sku, pricing.production, pricing.shipping, pricing.margin,
        pricing.overhead, pricing.discount,
        ))
    assert identical(pricing.pyre_derivations, (
        pricing.cost, pricing.msrp, pricing.price,
        ))

    return pricing


def identical(s1, s2):
    """
    Verify that the nodes in {s1} and {s2} are identical. This has to be done carefully since
    we must avoid triggering __eq__
    """
    for n1, n2 in zip(s1, s2):
        if n1 is not n2: return False
    return True
            

# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
