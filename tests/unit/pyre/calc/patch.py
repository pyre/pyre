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


import pyre.calc


def test():
    # the nodes
    production = pyre.calc.newNode(value = 80.)
    shipping = pyre.calc.newNode(value = 20.)
    cost = production + shipping
    margin = .25*cost
    overhead = .45*cost
    price = cost + margin + overhead
    discount = .2
    total = price*(1.0 - discount)

    print("Node@0x{0:x}".format(id(cost)))
    print("   value: {}".format(cost._value))
    print("   evaluator: {}".format(cost._evaluator))
    print("       _op1: {}".format(cost._evaluator._op1))
    print("       _op2: {}".format(cost._evaluator._op2))
    print("   observers:")
    for idx,observer in enumerate(cost._observers):
        print("       {}: {}".format(idx, observer))
        print("           node: {}".format(observer.__self__))
        print("           func: {}".format(observer.__func__))

    poser = pyre.calc.newNode()
    print("Node@0x{0:x}".format(id(poser)))
    print("   value: {}".format(poser._value))
    print("   evaluator: {}".format(poser._evaluator))

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
    assert set(Node._pyre_extent) == set()
    # for evaluators
    from pyre.calc.Evaluator import Evaluator
    assert set(Evaluator._pyre_extent) == set()


# end of file 
