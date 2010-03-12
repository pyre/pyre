#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify nodes with aggregator evaluators
"""


import pyre.calc


def test():
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
    # get the extent manager
    from pyre.patterns.ExtentAware import ExtentAware
    # install it
    pyre.calc._metaclass_Node = pyre.calc._metaclass_Evaluator = ExtentAware
    # run the test
    test()
    # verify reference counts
    # for nodes
    from pyre.calc.Node import Node
    # print([node for node in Node._pyre_extent])
    assert set(Node._pyre_extent) == set()
    # for evaluators
    from pyre.calc.Evaluator import Evaluator
    # print([evaluator for evaluator in Evaluator._pyre_extent])
    assert set(Evaluator._pyre_extent) == set()


# end of file 
