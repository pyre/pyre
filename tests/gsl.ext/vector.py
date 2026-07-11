#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the bound {Vector} directly, through the extension rather than the {gsl.vector} shim,
so a failure isolates the c++ layer
"""


def raises(fn, kind):
    """
    Return True if calling {fn} raises {kind}
    """
    # try the call
    try:
        # which is expected to fail
        fn()
    # if it raises the right thing
    except kind:
        # good
        return True
    # otherwise it did not guard
    return False


def test():
    # the bindings
    from gsl import libgsl

    # allocation and shape
    v = libgsl.Vector(shape=5)
    assert v.shape == 5
    assert len(v) == 5

    # initialization and access
    v.fill(2.0)
    assert v.get(3) == 2.0
    v.set(3, 9.0)
    assert v.get(3) == 9.0
    v.zero()
    assert v.get(0) == 0.0

    # the basis vector
    v.basis(2)
    assert v.get(2) == 1.0 and v.get(0) == 0.0

    # a negative index reflects; out of range and too-negative raise
    v.fill(1.0)
    v.set(-1, 4.0)
    assert v.get(-1) == 4.0
    assert raises(lambda: v.get(5), IndexError)
    assert raises(lambda: v.set(5, 0.0), IndexError)
    assert raises(lambda: v.get(-6), IndexError)
    assert raises(lambda: v.basis(5), IndexError)

    # copy and equality
    w = libgsl.Vector(shape=5).fill(3.0)
    v.copy(w)
    assert v.equal(w)
    assert not v.equal(libgsl.Vector(shape=5).fill(0.0))

    # containment and the cells as a tuple
    assert v.contains(3.0)
    assert not v.contains(7.0)
    assert v.tuple() == (3.0, 3.0, 3.0, 3.0, 3.0)

    # elementwise arithmetic, in place
    v.fill(2.0)
    v.add(libgsl.Vector(shape=5).fill(1.0))
    assert v.get(0) == 3.0
    v.scale(2.0)
    assert v.get(0) == 6.0
    v.shift(-1.0)
    assert v.get(0) == 5.0

    # extrema over a known pattern
    for i in range(5):
        v.set(i, float(i))
    assert v.max() == 4.0
    assert v.min() == 0.0
    assert v.minmax() == (0.0, 4.0)

    # statistics; the mean of 0..4 is 2, the sample variance is 2.5
    assert v.mean() == 2.0
    assert abs(v.variance() - 2.5) < 1e-12

    # the buffer protocol hands numpy a zero-copy view
    import numpy

    a = numpy.asarray(v)
    assert a.shape == (5,)
    a[0] = -1.0
    assert v.get(0) == -1.0

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
