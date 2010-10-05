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
    model["production"] = 80.
    model["shipping"] = 20
    model["cost"] = model.resolve("production") + model.resolve("shipping")
    model["margin"] = ".25*{cost}"
    model["overhead"] = ".45*{cost}"
    model["price"] = "{cost}+{margin}+{overhead}"
    model["discount"] = .2
    model["total"] = "{price}*(1.0 - {discount})"

    # check
    assert model["production"] == 80
    assert model["shipping"] == 20
    assert model["cost"] == model["production"] + model["shipping"]
    assert model["margin"] == .25*model["cost"]
    assert model["overhead"] == .45*model["cost"]
    assert model["price"] == model["margin"]+model["overhead"]+model["cost"]
    assert model["discount"] == .2
    assert model["total"] == (1-model["discount"])*model["price"]
    
    # change and check
    newcost = 100.
    model["production"] = newcost
    assert model["production"] == newcost
    assert model["shipping"] == 20
    assert model["cost"] == model["production"] + model["shipping"]
    assert model["margin"] == .25*model["cost"]
    assert model["overhead"] == .45*model["cost"]
    assert model["price"] == model["margin"]+model["overhead"]+model["cost"]
    assert model["discount"] == .2
    assert model["total"] == (1-model["discount"])*model["price"]
    
    # change and check again
    newdiscount = .45
    model["discount"] = newdiscount
    assert model["production"] == newcost
    assert model["shipping"] == 20
    assert model["cost"] == model["production"] + model["shipping"]
    assert model["margin"] == .25*model["cost"]
    assert model["overhead"] == .45*model["cost"]
    assert model["price"] == model["margin"]+model["overhead"]+model["cost"]
    assert model["discount"] == newdiscount
    assert model["total"] == (1-model["discount"])*model["price"]

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
