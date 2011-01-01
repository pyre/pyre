#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Check that the refcount is zero after all nodes have gone out of scope
"""




def test():

    import pyre.calc
    n1 = pyre.calc.newNode()
    n2 = pyre.calc.newNode()

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
    # get access to the Node class
    from pyre.calc.Node import Node
    # verify reference counts
    # print(tuple(Node._pyre_extent))
    assert tuple(Node._pyre_extent) == ()


# end of file 
