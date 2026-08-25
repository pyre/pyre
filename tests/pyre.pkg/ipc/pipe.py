#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: verify that the pipe transport builds channel pairs
"""


def test():
    # get the package
    import pyre.ipc

    # make a pair of pipes
    ends = pyre.ipc.newPipe().open()
    # the pair unpacks in a fixed order
    parent, child = ends
    # that matches its named endpoints
    assert ends.parent is parent
    assert ends.child is child

    # and hand it back
    return ends


# main
if __name__ == "__main__":
    test()


# end of file
