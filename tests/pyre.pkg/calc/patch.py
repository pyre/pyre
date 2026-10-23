#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a node spliced into an evaluation network takes over the place of the node it
replaces
"""


def test():
    # access the package
    import pyre.calc

    # the nodes
    production = pyre.calc.var(value=80.0)
    # the shipping cost
    shipping = pyre.calc.var(value=20.0)
    # the cost adds them up
    cost = production + shipping
    # the margin is a fraction of the cost
    margin = 0.25 * cost
    # and so is the overhead
    overhead = 0.45 * cost
    # the price adds up the cost, the margin and the overhead
    price = cost + margin + overhead
    # a plain number for the discount
    discount = 0.2
    # the total is the discounted price
    total = price * (1.0 - discount)
    # check we got the answer right
    assert total.value == 136
    # the poser
    poser = pyre.calc.var(value=180.0)

    # introduce the cast

    # patch cost with the new production node
    poser.replace(production)
    # check
    assert cost.value == poser.value + shipping.value
    # the margin follows the cost
    assert margin.value == 0.25 * cost.value
    # and so does the overhead
    assert overhead.value == 0.45 * cost.value
    # the price
    assert price.value == cost.value + margin.value + overhead.value
    # and the total
    assert total.value == price.value * (1.0 - discount)
    # check we got the new answer right
    assert total.value == 272

    # make an adjustment
    poser.value = 80
    # check
    assert cost.value == poser.value + shipping.value
    # the margin follows the cost
    assert margin.value == 0.25 * cost.value
    # and so does the overhead
    assert overhead.value == 0.45 * cost.value
    # the price
    assert price.value == cost.value + margin.value + overhead.value
    # and the total
    assert total.value == price.value * (1.0 - discount)
    # check we got the answer right
    assert total.value == 136

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
