#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that model initialization fails correctly in the presence of expressions that cannot be
evaluated even though they have no syntax errors
"""


import pyre.calc


def test():
    # a model
    model = pyre.calc.newModel(name="syntax")
    # the nodes
    production = pyre.calc.newNode(value=80.)
    shipping = pyre.calc.newNode(value=20.)
    cost = pyre.calc.newNode(
        value=pyre.calc.expression(formula="{production}&{shipping}", model=model))

    model.registerNode(name="production", node=production)
    model.registerNode(name="shipping", node=shipping)
    model.registerNode(name="cost", node=cost)

    try:
        cost.value
        assert False
    except cost.EvaluationError as error:
        pass

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
