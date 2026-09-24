#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
In-place arithmetic on managed grids happens on the device, without waiting; after a
synchronize, the cells agree with numpy

the host must not touch managed memory while the device is working on it, so every check
below synchronizes before it reads
"""


def test():
    import numpy
    import pyre.grid

    rng = numpy.random.default_rng(0)

    # a representative of each family of cell types
    for cell, dtype in [
        ("float32", numpy.float32),
        ("complex128", numpy.complex128),
        ("int64", numpy.int64),
        ("uint8", numpy.uint8),
    ]:
        integer = numpy.issubdtype(dtype, numpy.integer)
        # two grids, big enough to span several blocks
        x = pyre.grid.managed(shape=(300, 500), cell=cell)
        y = pyre.grid.managed(shape=(300, 500), cell=cell)
        X, Y = numpy.asarray(x), numpy.asarray(y)
        X[...] = (rng.random((300, 500)) * 10 + 1).astype(dtype)
        Y[...] = (rng.random((300, 500)) * 10 + 1).astype(dtype)
        # copies for numpy to work on, taken before the device gets going
        expected, other = X.copy(), Y.copy()
        s = 3 if integer else 1.5
        # the grid operators, back to back on the device
        x += y
        x += s
        x -= y
        x -= s
        x *= y
        x *= s
        if not integer:
            x /= y
            x /= s
        # wait for them
        pyre.grid.synchronize()
        # numpy's turn
        expected += other
        expected += dtype(s)
        expected -= other
        expected -= dtype(s)
        expected *= other
        expected *= dtype(s)
        if not integer:
            expected /= other
            expected /= dtype(s)
        # integers wrap around exactly like numpy's; the rest agree to roundoff
        if integer:
            assert (X == expected).all()
        else:
            assert numpy.allclose(X, expected, rtol=1e-5)

    # sub-grids on the device
    g = pyre.grid.managed(shape=(6, 8), cell="float64")
    g[1:, 2:] += 1.0
    g[0] += 5.0
    g[::2, ::3] *= 2.0
    pyre.grid.synchronize()
    expected = numpy.zeros((6, 8))
    expected[1:, 2:] += 1
    expected[0] += 5
    expected[::2, ::3] *= 2
    assert (numpy.asarray(g) == expected).all()

    # the device can't reach heap cells
    try:
        g += pyre.grid.heap(shape=(6, 8), cell="float64")
    except TypeError:
        pass
    else:
        assert False, "a managed grid took a heap grid"

    # the host path waits for the device before it reads managed cells
    m = pyre.grid.managed(shape=(4,), cell="float64")
    numpy.asarray(m)[...] = 2
    h = pyre.grid.heap(shape=(4,), cell="float64")
    numpy.asarray(h)[...] = 1
    m *= 3.0
    h += m
    assert (numpy.asarray(h) == 7).all()

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
