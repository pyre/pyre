#!/usr/bin/env python3
# -*- python -*-
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
    # on both sides
    assert ends.child is child
    # both ends are live
    assert parent.fileno() >= 0
    # each one of them
    assert child.fileno() >= 0
    # each end reads and writes through its one descriptor
    assert parent.inbound == parent.fileno()
    # in both directions
    assert parent.outbound == parent.fileno()
    # which is all it is made of
    assert parent.descriptors() == [parent.fileno()]

    # and hand them back
    return ends


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
