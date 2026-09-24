#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
In-place arithmetic on heap grids happens on the host, and agrees with numpy: with grids and
scalars, over every family of cell types, and through sub-grids
"""


def test():
    import numpy
    import pyre.grid

    rng = numpy.random.default_rng(0)

    # a representative of each family of cell types
    for cell, dtype in [
        ("float64", numpy.float64),
        ("complex64", numpy.complex64),
        ("int16", numpy.int16),
        ("uint32", numpy.uint32),
    ]:
        integer = numpy.issubdtype(dtype, numpy.integer)
        # two grids, filled through their numpy views
        x = pyre.grid.heap(shape=(5, 7), cell=cell)
        y = pyre.grid.heap(shape=(5, 7), cell=cell)
        X, Y = numpy.asarray(x), numpy.asarray(y)
        X[...] = (rng.random((5, 7)) * 10 + 1).astype(dtype)
        Y[...] = (rng.random((5, 7)) * 10 + 1).astype(dtype)
        # what numpy makes of the same sequence
        expected = X.copy()
        s = 3 if integer else 1.5
        # the grid operators hand back the grid itself
        z = x
        z += y
        assert z is x
        x += s
        x -= y
        x -= s
        x *= y
        x *= s
        expected += Y
        expected += dtype(s)
        expected -= Y
        expected -= dtype(s)
        expected *= Y
        expected *= dtype(s)
        # integer cells can't hold a quotient
        if not integer:
            x /= y
            x /= s
            expected /= Y
            expected /= dtype(s)
        # integers wrap around exactly like numpy's; the rest agree to roundoff
        if integer:
            assert (X == expected).all()
        else:
            assert numpy.allclose(X, expected)

    # sub-grids, including the write back that ends an augmented assignment on one
    g = pyre.grid.heap(shape=(6, 8), cell="float64")
    G = numpy.asarray(g)
    G[...] = 0
    g[1:, 2:] += 1.0
    g[0] += 5.0
    g[::2, ::3] *= 2.0
    expected = numpy.zeros((6, 8))
    expected[1:, 2:] += 1
    expected[0] += 5
    expected[::2, ::3] *= 2
    assert (G == expected).all()

    # the mistakes numpy would also refuse
    def refuses(error, action):
        try:
            action()
        except error:
            return True
        return False

    i = pyre.grid.heap(shape=(4,), cell="int32")
    f = pyre.grid.heap(shape=(4,), cell="float64")
    assert refuses(TypeError, lambda: i.__itruediv__(2))
    assert refuses(TypeError, lambda: i.__iadd__(1.5))
    assert refuses(TypeError, lambda: f.__iadd__(1j))
    assert refuses(ValueError, lambda: pyre.grid.heap(shape=(4,), cell="uint8").__iadd__(300))
    assert refuses(ValueError, lambda: f.__iadd__(pyre.grid.heap(shape=(5,), cell="float64")))
    assert refuses(TypeError, lambda: f.__iadd__(pyre.grid.heap(shape=(4,), cell="float32")))
    # views that share cells in different places would step on each other
    v = pyre.grid.heap(shape=(8,), cell="float64")
    assert refuses(ValueError, lambda: v[1:].__iadd__(v[:-1]))
    # and operands that aren't numbers or grids are left for python to refuse
    assert f.__iadd__("a") is NotImplemented

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
