#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that node resolution works
"""


import pyre.calc


def test():
    # set up the model
    model = pyre.calc.newModel(name="expression")

    # the production node
    p = 80.
    production = pyre.calc.newNode(value=p)
    # production.dump("production")
    price = pyre.calc.newNode(value=pyre.calc.expression(formula="2*{production}", model=model))
    # price.dump("price")

    # ask for the price
    try:
        price.value
        assert False
    except price.UnresolvedNodeError:
        pass

    # register the nodes
    model.registerNode(name="price", node=price)
    model.registerNode(name="production", node=production)

    # ask for the price again
    assert production.value == p
    assert price.value == 2*production.value

    # make a change
    p = 100.
    production.value = p
    # chek again
    assert production.value == p
    assert price.value == 2*production.value

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
    # print(tuple(Node._pyre_extent))
    assert tuple(Node._pyre_extent) == ()
    # print(tuple(Node.Evaluator._pyre_extent))
    assert tuple(Node.Evaluator._pyre_extent) == ()


# end of file 
