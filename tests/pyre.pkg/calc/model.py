#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify a somewhat non-trivial evaluation network with a mix of node operations
"""


def test():
    # access the package
    import pyre.calc

    # build the model
    model = pyre.calc.model()

    # make a couple
    p = 80
    # of free variables
    s = 20
    # wrap the production cost in a node
    production = pyre.calc.var(value=p)
    # and the shipping cost in another
    shipping = pyre.calc.var(value=s)
    # the nodes
    model["production"] = production
    # register the shipping cost
    model["shipping"] = shipping
    # the cost is the sum of production and shipping
    model["cost"] = production + shipping
    # the margin is a fraction of the cost
    model["margin"] = model.expression(".25*{cost}")
    # and so is the overhead
    model["overhead"] = model.expression(".45*{cost}")
    # the price adds up the cost, the margin and the overhead
    model["price"] = model.expression("{cost}+{margin}+{overhead}")
    # register a raw value for the discount
    model["discount"] = 0.2
    # the total is the discounted price
    model["total"] = model.expression("{price}*(1.0 - {discount})")

    # check
    assert model["production"] == 80
    # the shipping cost
    assert model["shipping"] == 20
    # the cost
    assert model["cost"] == model["production"] + model["shipping"]
    # the margin
    assert model["margin"] == 0.25 * model["cost"]
    # the overhead
    assert model["overhead"] == 0.45 * model["cost"]
    # the price
    assert model["price"] == model["margin"] + model["overhead"] + model["cost"]
    # the discount
    assert model["discount"] == 0.2
    # and the total
    assert model["total"] == (1 - model["discount"]) * model["price"]

    # change and check
    newcost = 100.0
    # raise the production cost
    model["production"] = newcost
    # verify the production cost took the new value
    assert model["production"] == newcost
    # the shipping cost is unaffected
    assert model["shipping"] == 20
    # the cost follows the production cost
    assert model["cost"] == model["production"] + model["shipping"]
    # and so does the margin
    assert model["margin"] == 0.25 * model["cost"]
    # the overhead
    assert model["overhead"] == 0.45 * model["cost"]
    # the price
    assert model["price"] == model["margin"] + model["overhead"] + model["cost"]
    # the discount is unaffected
    assert model["discount"] == 0.2
    # and the total follows the price
    assert model["total"] == (1 - model["discount"]) * model["price"]

    # change and check again
    newdiscount = 0.45
    # replace the discount
    model["discount"] = newdiscount
    # the production cost is unaffected
    assert model["production"] == newcost
    # so is the shipping cost
    assert model["shipping"] == 20
    # the cost
    assert model["cost"] == model["production"] + model["shipping"]
    # the margin
    assert model["margin"] == 0.25 * model["cost"]
    # the overhead
    assert model["overhead"] == 0.45 * model["cost"]
    # and the price
    assert model["price"] == model["margin"] + model["overhead"] + model["cost"]
    # verify the discount took the new value
    assert model["discount"] == newdiscount
    # and the total follows the discount
    assert model["total"] == (1 - model["discount"]) * model["price"]

    # all done
    return


# main
if __name__ == "__main__":
    # request debugging support for the pyre.calc package
    pyre_debug = {"pyre.calc"}
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()
    # verify reference counts
    # for nodes
    from pyre.calc.Node import Node

    # no node outlives the test
    assert tuple(Node.pyre_extent) == ()


# end of file
