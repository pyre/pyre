#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify container nodes
"""


def test():
    # access the package
    import pyre.calc

    # make some nodes
    nodes = []
    # holding the integers from one through ten
    for n in range(10):
        # make a variable with the next integer
        node = pyre.calc.var(value=n + 1)
        # and add it to the pile
        nodes.append(node)

    # make a sequence
    s = pyre.calc.sequence(*nodes)
    # check
    assert tuple(s.value) == tuple(range(1, 11))

    # make a mapping
    m = pyre.calc.mapping(**{f"n{i}": n for i, n in enumerate(nodes)})
    # check
    assert m.value == dict({f"n{i}": i + 1 for i in range(10)})

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
