#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify nodes with sum evaluators
"""


import pyre.calc


def test():

    # set up the values
    p = 80.
    s = 20.
    # make the nodes
    production = pyre.calc.newNode(value=p)
    shipping = pyre.calc.newNode(value=s)
    cost = pyre.calc.newNode(value=pyre.calc.sum(production, shipping))

    # gather them up
    nodes = [production, shipping, cost]

    # check 
    assert production.value == p
    assert shipping.value == s
    assert cost.value == p + s

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
    # print([node for node in Node._pyre_extent])
    assert set(Node._pyre_extent) == set()
    # for evaluators
    from pyre.calc.Evaluator import Evaluator
    # print([evaluator for evaluator in Evaluator._pyre_extent])
    assert set(Evaluator._pyre_extent) == set()


# end of file 
