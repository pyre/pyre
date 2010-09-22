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


def test():
    import pyre.calc

    # build the model
    model = pyre.calc.newModel(name="sample")

    # the nodes
    production = 80.
    model["production"] = production
    model["shipping"] = 20.
    model["cost"] = model["production"] + model["shipping"]
    model["margin"] = ".25*{cost}"
    model["overhead"] = ".45*{cost}"
    model["price"] = pyre.calc.sum(model["cost"], model["margin"], model["overhead"])
    model["discount"] = .2
    model["total"] = "{price}*(1.0 - {discount})"

    # check the final answer
    assert model["total"].value == 136

    # check the partial results
    assert model["production"].value == 80
    assert model["shipping"].value == 20
    assert model["cost"].value == model["production"].value + model["shipping"].value
    assert model["margin"].value == .25*model["cost"].value
    assert model["overhead"].value == .45*model["cost"].value
    assert model["price"].value == model["margin"].value+model["overhead"].value+model["cost"].value
    assert model["discount"].value == .2
    assert model["total"].value == (1-model["discount"].value)*model["price"].value
    
    # change and check again
    production = 180.
    model["production"] = production
    # check the new final answer
    assert model["total"].value == 272
    # check the partial results
    assert model["production"].value == production
    assert model["shipping"].value == 20
    assert model["cost"].value == model["production"].value + model["shipping"].value
    assert model["margin"].value == .25*model["cost"].value
    assert model["overhead"].value == .45*model["cost"].value
    assert model["price"].value == model["margin"].value+model["overhead"].value+model["cost"].value
    assert model["discount"].value == .2
    assert model["total"].value == (1-model["discount"].value)*model["price"].value
    
    # change and check again
    discount = .50
    model["discount"] = discount
    # check the new final answer
    assert model["total"].value == 170
    # check the partial results
    assert model["production"].value == production
    assert model["shipping"].value == 20
    assert model["cost"].value == model["production"].value + model["shipping"].value
    assert model["margin"].value == .25*model["cost"].value
    assert model["overhead"].value == .45*model["cost"].value
    assert model["price"].value == model["margin"].value+model["overhead"].value+model["cost"].value
    assert model["discount"].value == discount
    assert model["total"].value == (1-model["discount"].value)*model["price"].value

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
