#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
In-place arithmetic between two heap grids agrees with numpy
"""


def test():
    # support
    import numpy
    import pyre.grid

    # two grids
    x = pyre.grid.heap(shape=(5, 7), cell="float64")
    y = pyre.grid.heap(shape=(5, 7), cell="float64")
    # filled with known values
    numpy.asarray(x)[...] = numpy.arange(35).reshape(5, 7) + 1
    numpy.asarray(y)[...] = 2.0
    # what numpy makes of the same sequence
    expected = (((numpy.arange(35).reshape(5, 7) + 1 + 2) - 2) * 2) / 2
    # the operators hand back the grid itself
    z = x
    z += y
    assert z is x
    # and the rest of the sequence
    x -= y
    x *= y
    x /= y
    # agree with numpy
    assert (numpy.asarray(x) == expected).all()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
