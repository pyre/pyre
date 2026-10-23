#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify nodes with sum evaluators
"""


def test():
    # access the package
    import pyre.calc

    # set up the values
    p = 80.0
    # of the production and shipping costs
    s = 20.0
    # make the nodes
    production = pyre.calc.var(value=p)
    # one for the shipping cost
    shipping = pyre.calc.var(value=s)
    # the cost adds them up
    cost = pyre.calc.sum(production, shipping)
    # and a reference to the cost
    clone = cost.ref()

    # check the dependencies
    assert tuple(cost.operands) == (production, shipping)
    # the reference depends on the cost alone
    assert tuple(clone.operands) == (cost,)
    # and the dependents
    assert set(production.observers) == {cost}
    # the cost observes the shipping cost
    assert set(shipping.observers) == {cost}
    # and the reference observes the cost
    assert set(cost.observers) == {clone}
    # check the values
    assert production.value == p
    # the shipping cost
    assert shipping.value == s
    # the cost is the sum
    assert cost.value == p + s
    # and the reference sees the sum
    assert clone.value == p + s

    # update the values
    p = 160.0
    # of both costs
    s = 40.0
    # push the new production cost to its node
    production.value = p
    # and the new shipping cost to its own
    shipping.value = s

    # check again
    assert production.value == p
    # the shipping cost
    assert shipping.value == s
    # the cost follows the change
    assert cost.value == p + s
    # and so does the reference
    assert clone.value == p + s

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
