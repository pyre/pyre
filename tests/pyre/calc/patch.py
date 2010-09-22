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

    # the nodes
    production = pyre.calc.newNode(value = 80.)
    shipping = pyre.calc.newNode(value = 20.)
    cost = production + shipping
    margin = .25*cost
    overhead = .45*cost
    price = cost + margin + overhead
    discount = .2
    total = price*(1.0 - discount)
    # check we got the answer right
    assert total.value == 136
    # the poser
    poser = pyre.calc.newNode(value=180.)

    # introduce the cast
    # print("production: node@{:#x}".format(id(production)))
    # print("  shipping: node@{:#x}".format(id(shipping)))
    # print("      cost: node@{:#x}".format(id(cost)))
    # print("    margin: node@{:#x}".format(id(margin)))
    # print("  overhead: node@{:#x}".format(id(overhead)))
    # print("     price: node@{:#x}".format(id(price)))
    # print("  discount: node@{:#x}".format(id(discount)))
    # print("     total: node@{:#x}".format(id(total)))
    # print("     poser: node@{:#x}".format(id(poser)))

    # patch cost with the new production node
    cost.patch(old=production, new=poser)
    # check
    # assert cost.value == poser.value + shipping.value
    # assert margin.value == .25*cost.value
    # assert overhead.value == .45*cost.value
    # assert price.value  == cost.value + margin.value + overhead.value
    # assert total.value == price.value*(1.0 - discount)
    # check we got the new answer right
    assert total.value == 272

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
