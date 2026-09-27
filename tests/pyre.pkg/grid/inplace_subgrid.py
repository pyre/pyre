#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
In-place arithmetic on a sub-grid changes the cells it views, and only those
"""


def test():
    # support
    import numpy
    import pyre.grid

    # a grid
    g = pyre.grid.heap(shape=(6, 8), cell="float64")
    # filled with zeros, since nobody wrote it yet
    numpy.asarray(g)[...] = 0
    # a block, a row, and a strided view
    g[1:, 2:] += 1.0
    g[0] += 5.0
    g[::2, ::3] *= 2.0
    # what numpy makes of the same sequence
    expected = numpy.zeros((6, 8))
    expected[1:, 2:] += 1
    expected[0] += 5
    expected[::2, ::3] *= 2
    # agrees with the grid
    assert (numpy.asarray(g) == expected).all()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
