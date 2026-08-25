#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: verify that the socket transport builds channel pairs
"""


def test():
    # get the package
    import pyre.ipc

    # make a pair of connected channels
    ends = pyre.ipc.newSocket().open()
    # the pair unpacks in a fixed order
    parent, child = ends
    # that matches its named endpoints
    assert ends.parent is parent
    assert ends.child is child
    # both ends are live
    assert parent.fileno() >= 0
    assert child.fileno() >= 0
    # each end serves as both the inbound and the outbound endpoint
    assert parent.inbound is parent
    assert parent.outbound is parent

    # and hand them back
    return ends


# main
if __name__ == "__main__":
    test()


# end of file
