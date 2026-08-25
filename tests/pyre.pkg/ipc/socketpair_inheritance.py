#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the two ends of a socket pair honor the {Pipe} inheritance contract
"""


def test():
    # get the package
    import pyre.ipc

    # make a pair of connected channels
    parent, child = pyre.ipc.newSocket().open()
    # the parent end must not survive an {exec}
    assert parent.get_inheritable() is False
    # while the child end must, so it can be handed to a freshly spawned process
    assert child.get_inheritable() is True

    # all done
    return parent, child


# main
if __name__ == "__main__":
    test()


# end of file
