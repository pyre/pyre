#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that node resolution works
"""


def test():
    import pyre.calc

    # set up the model
    model = pyre.calc.model(name="expression")

    # set up an expression with an unresolved node
    model["price"] = "2*{production}"

    # ask for the price
    try:
        model["price"]
        assert False
    except model.UnresolvedNodeError as error:
        unresolved, _ = model._resolve(name="production")
        assert error.node is unresolved
        assert error.name == "production"

    # resolve the node
    p = 80.
    model["production"] = p

    # ask for the price again
    assert model["production"] == p
    assert model["price"] == 2*p

    # make a change
    p = 100.
    model["production"] = p
    # chek again
    assert model["production"] == p
    assert model["price"] == 2*p

    # force a node substitution
    m = 60
    model["materials"] = m
    model["production"] = "2*{materials}"
    # chek again
    assert model["materials"] == m
    assert model["production"] == 2*m
    assert model["price"] == 4*m

    return


# main
if __name__ == "__main__":
    # request debugging support for the pyre.calc package
    pyre_debug = { "pyre.calc" }
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()
    # verify reference counts
    # for nodes
    from pyre.calc.Node import Node
    # print(tuple(Node._pyre_extent))
    assert tuple(Node._pyre_extent) == ()


# end of file 
