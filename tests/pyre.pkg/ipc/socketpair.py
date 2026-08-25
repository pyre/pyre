#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: verify that the socketpair factory is accessible
"""


def test():
    # get the package
    import pyre.ipc

    # make a pair of connected channels
    parent, child = pyre.ipc.socketpair()
    # both ends are live
    assert parent.fileno() >= 0
    assert child.fileno() >= 0
    # each end serves as both the inbound and the outbound endpoint
    assert parent.inbound is parent
    assert parent.outbound is parent

    # and hand them back
    return parent, child


# main
if __name__ == "__main__":
    test()


# end of file
