#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
In-place arithmetic takes any buffer of the right shape and cell type, such as a numpy array
"""


def test():
    # support
    import numpy
    import pyre.grid

    # a grid
    x = pyre.grid.heap(shape=(3, 4), cell="float64")
    # filled with known values
    numpy.asarray(x)[...] = numpy.arange(12).reshape(3, 4)
    # combined with a numpy array
    x += numpy.full((3, 4), 0.5)
    # agrees with numpy
    assert (numpy.asarray(x) == numpy.arange(12).reshape(3, 4) + 0.5).all()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
