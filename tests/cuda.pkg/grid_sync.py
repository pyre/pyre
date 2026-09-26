#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The host waits for the device before it reaches the cells of a managed grid
"""


def test():
    # support
    import numpy
    import pyre.cuda

    # a managed grid
    g = pyre.cuda.managed(shape=(1000, 1000), cell="float64")
    # filled with known values
    numpy.asarray(g)[...] = 1
    # a sequence of operations queued on the device, with no explicit synchronization
    for _ in range(10):
        # each one doubles the cells
        g *= 2.0
    # reading a cell waits for the device
    assert g[999, 999] == 1024.0
    # and so does a view of the cells
    assert (numpy.asarray(g) == 1024.0).all()
    # explicit synchronization is harmless
    pyre.cuda.synchronize()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
