#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
In-place arithmetic on managed grids runs on the device and agrees with numpy
"""


def test():
    # support
    import numpy
    import pyre.cuda

    # a representative of each family of cell types
    for cell in ("float32", "complex128", "int64", "uint8"):
        # the numpy spelling of the cell type
        dtype = numpy.dtype(cell)
        # whether the cells are integers
        integer = numpy.issubdtype(dtype, numpy.integer)
        # two grids, large enough to span several blocks
        x = pyre.cuda.managed(shape=(300, 500), cell=cell)
        y = pyre.cuda.managed(shape=(300, 500), cell=cell)
        # filled with known values
        numpy.asarray(x)[...] = (numpy.arange(150000).reshape(300, 500) % 7 + 1).astype(dtype)
        numpy.asarray(y)[...] = 2
        # what numpy makes of the same sequence
        expected = numpy.asarray(x).copy()
        # the scalar operand
        s = 3 if integer else 1.5
        # the grid operators, on the device
        x += y
        x *= s
        x -= y
        # and the same on the host
        expected += 2
        expected *= dtype.type(s)
        expected -= 2
        # agree, once the host reads the cells
        assert numpy.allclose(numpy.asarray(x), expected, rtol=1e-5)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
