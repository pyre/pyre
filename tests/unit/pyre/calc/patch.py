#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify a somewhat non-trivial evaluation network with a mix of node operations
"""


import pyre.calc


def test():
    # the nodes
    production = pyre.calc.newNode(value = 80.)
    shipping = pyre.calc.newNode(value = 20.)
    cost = production + shipping
    margin = .25*cost
    overhead = .45*cost
    price = cost + margin + overhead
    discount = .2
    total = price*(1.0 - discount)
    # the poser
    poser = pyre.calc.newNode(value=150.)
    # need a name to patch expressions
    poser.replace(node=cost)
    # check
    assert margin.value == .25*poser.value
    assert overhead.value == .45*poser.value
    assert price.value  == poser.value + margin.value + overhead.value
    assert total.value == price.value*(1.0 - discount)

    return


# main
if __name__ == "__main__":
    # get the extent manager
    from pyre.patterns.ExtentAware import ExtentAware
    # install it
    pyre.calc._metaclass_Node = pyre.calc._metaclass_Evaluator = ExtentAware
    # run the test
    test()
    # verify reference counts
    # for nodes
    from pyre.calc.Node import Node
    # print(set(Node._pyre_extent))
    assert set(Node._pyre_extent) == set()
    # for evaluators
    from pyre.calc.Evaluator import Evaluator
    # print(set(Evaluator._pyre_extent))
    assert set(Evaluator._pyre_extent) == set()


# end of file 
