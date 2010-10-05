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


def test():
    import pyre.calc

    # set up the model
    model = pyre.calc.newModel(name="expression")

    # set up an expression with an unresolved node
    model["price"] = "2*{production}"

    # ask for the price
    try:
        model["price"]
        assert False
    except model.UnresolvedNodeError as error:
        assert error.node == model.resolve(name="price")
        assert error.name == "production"

    # resovle the node
    p = 80.
    model["production"] = p

    # ask for the price again
    assert model["production"] == p
    assert model["price"] == 2*model["production"]

    # make a change
    p = 100.
    model["production"] = p
    # chek again
    assert model["production"] == p
    assert model["price"] == 2*model["production"]

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
