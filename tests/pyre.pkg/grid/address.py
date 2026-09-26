#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A grid publishes the address of its first cell, the one its buffer view starts at
"""


def test():
    # support
    import numpy
    import pyre.grid

    # make a grid
    g = pyre.grid.heap(shape=(3, 4), cell="float64")
    # its address is the one its buffer view sees
    assert g.address == numpy.asarray(g).ctypes.data
    # and a sub-grid starts at its own first cell
    assert g[1:, 2:].address - g.address == (1 * 4 + 2) * 8

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
