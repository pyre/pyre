#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify on-the-fly building of nodes using the overloaded operators
"""


def test():
    import pyre.calc

    # free variables
    c = 100.
    s = 20.

    # make some nodes
    cost = pyre.calc.newNode(value=c)
    shipping = pyre.calc.newNode(value=s)
    margin = cost / 2
    price = cost + margin + shipping
    profit = price - margin

    # gather them up
    nodes = [ cost, shipping, margin, price, profit ]

    # verify their values
    # print(cost.value, shipping.value, margin.value, price.value, profit.value)
    assert cost.value == c
    assert shipping.value == s
    assert margin.value == .5*cost.value
    assert price.value == cost.value + shipping.value + margin.value
    assert profit.value == price.value - margin.value

    # make some changes
    c = 200.
    s = 40.
    cost.value = c
    shipping.value = s

    # try again
    # print(cost.value, shipping.value, margin.value, price.value, profit.value)
    assert cost.value == c
    assert shipping.value == s
    assert margin.value == .5*cost.value
    assert price.value == cost.value + shipping.value + margin.value
    assert profit.value == price.value - margin.value

    return


# main
if __name__ == "__main__":
    # request debugging support for the pyre.calc package
    pyre_debug = { "pyre.calc" }
    # run the test
    test()
    # destroy the framework parts to make sure there are no excess nodes around
    import pyre
    pyre.shutdown()
    # verify reference counts
    # for nodes
    from pyre.calc.Node import Node
    # print(tuple(Node._pyre_extent))
    assert tuple(Node._pyre_extent) == ()
    # print(tuple(Node.Evaluator._pyre_extent))
    assert tuple(Node.Evaluator._pyre_extent) == ()


# end of file 
