#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that reference nodes correctly reflect the value of their referends
"""


def test():
    import pyre.calc

    # make a node and set its value
    v = 80.
    production = pyre.calc.newNode(value=v)
    clone = pyre.calc.newNode(value=production.newReference())

    assert production.value == v
    assert clone.value == v
    
    # once more
    v = 100.
    production.value = v
    assert production.value == v
    assert clone.value == v

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
