#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a manifest leaves everything other than channels to the marshaler
"""


def test():
    # access the package
    import pyre.ipc

    # make a manifest
    manifest = pyre.ipc.manifest()
    # go through a few values that are not channels
    for value in (None, 0, "channel", b"\x00", [1, 2], {"kind": "pipe"}, pyre.ipc.newPipe()):
        # none of them is declared
        assert manifest.declare(value) is None
    # and no descriptors were collected
    assert manifest.descriptors == []

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
