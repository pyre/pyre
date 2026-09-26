#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a node can be added to a mapping after it is built
"""


def test():
    """
    Add a node to a mapping through its value and read it back
    """
    # get the package
    import pyre.calc

    # a mapping with a couple of entries
    m = pyre.calc.mapping(one=pyre.calc.var(value=1), two=pyre.calc.var(value=2))
    # add another one, as a {key, node} pair
    m.value = ("three", pyre.calc.var(value=3))
    # it is there, under its key
    assert m["three"] == 3
    # and the mapping reports all three
    assert m.value == {"one": 1, "two": 2, "three": 3}

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
    from pyre.calc.Node import Node

    # every node is gone
    assert tuple(Node.pyre_extent) == ()


# end of file
