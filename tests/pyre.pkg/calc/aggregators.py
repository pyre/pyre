#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify nodes with aggregator evaluators
"""


def test():
    # access the package
    import pyre.calc

    # make some nodes
    nodes = []
    # one for each of the first ten integers
    for n in range(10):
        # make a node that holds the integer
        node = pyre.calc.var(value=n)
        # and add it to the pile
        nodes.append(node)

    # count the nodes
    count = pyre.calc.count(*nodes)
    # add up their values
    sum = pyre.calc.sum(*nodes)
    # find the smallest value
    min = pyre.calc.min(*nodes)
    # and the largest
    max = pyre.calc.max(*nodes)
    # and compute the average
    average = pyre.calc.average(*nodes)

    # check the count
    assert count.value == 10
    # the sum
    assert sum.value == 45
    # the smallest value
    assert min.value == 0
    # the largest value
    assert max.value == 9
    # and the average
    assert average.value == 4.5

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
