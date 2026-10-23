#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that reference nodes correctly reflect the value of their referends
"""


def test():
    # access the package
    import pyre.calc

    # make a node and set its value
    v = 80.0
    # make a node that holds it
    production = pyre.calc.var(value=v)
    # make a reference
    clone = production.ref()
    # and a reference to the reference
    clone2 = clone.ref()

    # check the node
    assert production.value == v
    # the reference
    assert clone.value == v
    # and the reference to the reference
    assert clone2.value == v

    # once more, with a new value
    v = 100.0
    # hand it to the node
    production.value = v
    # check the node
    assert production.value == v
    # the reference sees the change
    assert clone.value == v
    # and so does the reference to the reference
    assert clone2.value == v

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
