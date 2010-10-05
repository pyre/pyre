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


def test():
    import pyre.calc

    # set up the model
    model = pyre.calc.newModel(name="expression")

    # the nodes
    p = 80.
    s = .25*80
    # register the nodes
    model["production"] = p
    model["shipping"] = s
    model["cost"] = "{production}+{shipping}"
    model["price"] = "2*{cost}"

    # check the values
    # print("before:")
    # print("  production:", model["production"])
    # print("  shipping:", model["shipping"])
    # print("  cost:", model["cost"])
    # print("  price:", model["price"])
    assert model["production"] == p
    assert model["shipping"] == s
    assert model["cost"] == model["production"] + model["shipping"]
    assert model["price"] == 2*model["cost"]

    # make a change
    p = 100.
    model["production"] = p

    # check again
    # print("after:")
    # print("  production:", production.value)
    # print("  shipping:", shipping.value)
    # print("  cost:", cost.value)
    # print("  price:", price.value)
    assert model["production"] == p
    assert model["shipping"] == s
    assert model["cost"] == model["production"] + model["shipping"]
    assert model["price"] == 2*model["cost"]

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
