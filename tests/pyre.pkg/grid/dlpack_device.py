#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A grid on host storage reports the host as its dlpack device
"""


def test():
    # support
    import pyre.grid

    # make a grid on the heap
    g = pyre.grid.heap(shape=(2, 3), cell="float64")
    # it lives on the host, device index zero
    assert g.__dlpack_device__() == (1, 0)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
