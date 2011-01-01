#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that model initialization fails correctly in the presence of expressions that cannot be
evaluated even though they have no syntax errors
"""


def test():
    import pyre.calc

    # a model
    model = pyre.calc.newModel(name="syntax")
    # the nodes
    production = pyre.calc.newNode(value=80.)
    shipping = pyre.calc.newNode(value=20.)
    cost = pyre.calc.newNode(
        value=pyre.calc.expression(formula="{production}&{shipping}", model=model))

    model.register(name="production", node=production)
    model.register(name="shipping", node=shipping)
    model.register(name="cost", node=cost)

    try:
        cost.value
        assert False
    except cost.EvaluationError as error:
        pass

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
