#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that expressions work
"""


import pyre.calc


def test():
    # set up the model
    model = pyre.calc.newModel(name="expression")

    # the nodes
    p = 80.
    s = .25*80
    production = pyre.calc.newNode(value=p)
    shipping = pyre.calc.newNode(value=s)
    cost = pyre.calc.newNode(
        value=pyre.calc.expression(formula="{production}+{shipping}", model=model))
    price = pyre.calc.newNode(value=pyre.calc.expression(formula="2*{cost}", model=model))

    # register the nodes
    model.registerNode(name="production", node=production)
    model.registerNode(name="shipping", node=shipping)
    model.registerNode(name="cost", node=cost)
    model.registerNode(name="price", node=price)

    # check the values
    assert production.value == p
    assert shipping.value == s
    assert cost.value == production.value + shipping.value
    assert price.value == 2*cost.value

    # make a change
    p = 100.
    production.value = p

    # chek again
    assert production.value == p
    assert shipping.value == s
    assert cost.value == production.value + shipping.value
    assert price.value == 2*cost.value

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
