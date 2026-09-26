#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the device manager finds the attached devices
"""


def test():
    # access the package
    import pyre.cuda

    # the tests run where the driver sees a device, so the manager finds at least one
    assert pyre.cuda.manager.count > 0
    # and describes each of them
    assert len(pyre.cuda.manager.devices) == pyre.cuda.manager.count

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
