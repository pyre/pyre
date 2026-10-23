#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify on-the-fly building of nodes using the overloaded operators
"""


def test():
    # access the package
    import pyre.calc

    # free variables
    c = 100.0
    # and the shipping cost
    s = 20.0

    # make some nodes
    cost = pyre.calc.var(value=c)
    # one for the shipping cost
    shipping = pyre.calc.var(value=s)
    # the margin is half the cost
    margin = cost / 2
    # the price adds up the cost, the margin and the shipping
    price = cost + margin + shipping
    # and the profit is what is left after the margin
    profit = price - margin

    # gather them up
    nodes = [cost, shipping, margin, price, profit]

    # verify their values
    assert cost.value == c
    # the shipping cost
    assert shipping.value == s
    # the margin
    assert margin.value == 0.5 * c
    # the price
    assert price.value == c + s + 0.5 * c
    # and the profit
    assert profit.value == c + s

    # make some changes
    c = 200.0
    # to both free variables
    s = 40.0
    # push the new cost to its node
    cost.value = c
    # and the new shipping cost to its own
    shipping.value = s

    # try again
    assert cost.value == c
    # the shipping cost
    assert shipping.value == s
    # the margin follows the cost
    assert margin.value == 0.5 * c
    # the price follows both
    assert price.value == c + s + 0.5 * c
    # and so does the profit
    assert profit.value == c + s

    # all done
    return


# main
if __name__ == "__main__":
    # request debugging support for the pyre.calc package
    pyre_debug = {"pyre.calc"}
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()
    # verify reference counts
    # for nodes
    from pyre.calc.Node import Node

    # no node outlives the test
    assert tuple(Node.pyre_extent) == ()


# end of file
