#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the device manager of a machine without devices finds none, rather than failing
"""


def test():
    # externals
    import os

    # hide the devices from the driver before anything reaches it
    os.environ["CUDA_VISIBLE_DEVICES"] = ""

    # framework
    import journal

    # the manager says it found no devices; silence it
    journal.warning("pyre.cuda.discovery").deactivate()

    # access the package
    import pyre.cuda

    # the manager finds no devices
    assert pyre.cuda.manager.count == 0
    # and describes none
    assert pyre.cuda.manager.devices == []

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
