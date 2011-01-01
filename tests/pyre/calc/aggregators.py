#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify nodes with aggregator evaluators
"""


def test():
    import pyre.calc

    # make some nodes
    nodes = []
    for n in range(10):
        node = pyre.calc.newNode(value=n)
        nodes.append(node)

    count = pyre.calc.newNode(value=pyre.calc.count(*nodes))
    sum = pyre.calc.newNode(value=pyre.calc.sum(*nodes))
    min = pyre.calc.newNode(value=pyre.calc.min(*nodes))
    max = pyre.calc.newNode(value=pyre.calc.max(*nodes))
    average = pyre.calc.newNode(value=pyre.calc.average(*nodes))
    
    # check
    assert count.value == 10
    assert sum.value == 45
    assert min.value == 0
    assert max.value == 9
    assert average.value == 4.5

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
