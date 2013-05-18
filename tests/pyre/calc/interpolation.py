#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Verify that interpolations work
"""


def test():
    import pyre.calc

    # set up the model
    model = pyre.calc.model()

    # the nodes
    home = "/home/first"
    tools = "tools"
    # register the nodes
    model["home"] = home
    model["tools"] = tools
    model["path"] = model.interpolation("{home}/{tools}")

    # check the values
    assert model["home"] == home
    assert model["tools"] == tools
    assert model["path"] == home + '/' + tools

    # make a change
    home = "/home/second"
    model["home"] = home

    # check again
    assert model["home"] == home
    assert model["tools"] == tools
    assert model["path"] == home + '/' + tools

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
