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

    # build the model
    model = pyre.calc.newModel(name="sample")

    # the nodes
    production = pyre.calc.newNode(value = 80.)
    shipping = pyre.calc.newNode(value = 20.)
    cost = production + shipping
    margin = pyre.calc.newNode(value=pyre.calc.expression(formula=".25*{cost}", model=model))
    overhead = pyre.calc.newNode(value=pyre.calc.expression(formula=".45*{cost}", model=model))
    price = pyre.calc.newNode(value=pyre.calc.sum(cost, margin, overhead))
    discount = pyre.calc.newNode(value = .2)
    total = pyre.calc.newNode(value=pyre.calc.expression(
            formula="{price}*(1.0 - {discount})", model=model))

    # register the nodes
    model.registerNode(node=production, name="production")
    model.registerNode(node=shipping, name="shipping")
    model.registerNode(node=cost, name="cost")
    model.registerNode(node=margin, name="margin")
    model.registerNode(node=overhead, name="overhead")
    model.registerNode(node=price, name="price")
    model.registerNode(node=discount, name="discount")
    model.registerNode(node=total, name="total")

    # check
    assert production.value == 80
    assert shipping.value == 20
    assert cost.value == production.value + shipping.value
    assert margin.value == .25*cost.value
    assert overhead.value == .45*cost.value
    assert price.value == margin.value+overhead.value+cost.value
    assert discount.value == .2
    assert total.value == (1-discount.value)*price.value
    
    # change and check
    newcost = 100.
    production.value = newcost
    assert production.value == newcost
    assert shipping.value == 20
    assert cost.value == production.value + shipping.value
    assert margin.value == .25*cost.value
    assert overhead.value == .45*cost.value
    assert price.value == margin.value+overhead.value+cost.value
    assert discount.value == .2
    assert total.value == (1-discount.value)*price.value
    
    # change and check again
    newdiscount = .45
    discount.value = newdiscount
    assert production.value == newcost
    assert shipping.value == 20
    assert cost.value == production.value + shipping.value
    assert margin.value == .25*cost.value
    assert overhead.value == .45*cost.value
    assert price.value == margin.value+overhead.value+cost.value
    assert discount.value == newdiscount
    assert total.value == (1-discount.value)*price.value

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
