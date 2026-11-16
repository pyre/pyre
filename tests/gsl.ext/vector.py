#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the bound {Vector} directly, through the extension rather than the {gsl.vector} shim,
so a failure isolates the c++ layer
"""


def raises(call, kind):
    """
    Return True if invoking {call} raises {kind}
    """
    # try the call
    try:
        # which is expected to fail
        call()
    # if it raises the right thing
    except kind:
        # good
        return True
    # otherwise it did not guard
    return False


def test():
    # the bindings
    from gsl import libgsl

    # make a vector
    vector = libgsl.Vector(shape=5)
    # and check its shape
    assert vector.shape == 5
    # and its length
    assert len(vector) == 5

    # fill it
    vector.fill(2.0)
    # and check that the cells were set
    assert vector.get(3) == 2.0
    # set one cell
    vector.set(3, 9.0)
    # and read it back
    assert vector.get(3) == 9.0
    # clear it
    vector.zero()
    # and check
    assert vector.get(0) == 0.0

    # make it a basis vector
    vector.basis(2)
    # with a one in its slot and zeroes elsewhere
    assert vector.get(2) == 1.0 and vector.get(0) == 0.0

    # a negative index counts from the end
    vector.fill(1.0)
    # so setting the last cell
    vector.set(-1, 4.0)
    # is visible through the same index
    assert vector.get(-1) == 4.0
    # indices past the end are refused when reading
    assert raises(lambda: vector.get(5), IndexError)
    # and when writing
    assert raises(lambda: vector.set(5, 0.0), IndexError)
    # as are negative indices that reach before the start
    assert raises(lambda: vector.get(-6), IndexError)
    # and basis vectors outside the shape
    assert raises(lambda: vector.basis(5), IndexError)

    # make another vector
    other = libgsl.Vector(shape=5).fill(3.0)
    # copy it into mine
    vector.copy(other)
    # after which the two are equal
    assert vector.equal(other)
    # and differ from a vector with other values
    assert not vector.equal(libgsl.Vector(shape=5).fill(0.0))

    # the vector contains the value it was filled with
    assert vector.contains(3.0)
    # and no other
    assert not vector.contains(7.0)
    # and hands its cells over as a tuple
    assert vector.tuple() == (3.0, 3.0, 3.0, 3.0, 3.0)

    # start with a known value
    vector.fill(2.0)
    # add another vector, in place
    vector.add(libgsl.Vector(shape=5).fill(1.0))
    # and check
    assert vector.get(0) == 3.0
    # scale it
    vector.scale(2.0)
    # and check
    assert vector.get(0) == 6.0
    # shift it
    vector.shift(-1.0)
    # and check
    assert vector.get(0) == 5.0

    # set the cells to 0..4
    for index in range(5):
        # one at a time
        vector.set(index, float(index))
    # the largest
    assert vector.max() == 4.0
    # the smallest
    assert vector.min() == 0.0
    # and both at once
    assert vector.minmax() == (0.0, 4.0)

    # the mean of 0..4 is 2
    assert vector.mean() == 2.0
    # weighted by the cells themselves, it is 30/10
    assert abs(vector.mean(weights=vector) - 3.0) < 1e-12
    # and the sample variance is 2.5
    assert abs(vector.variance() - 2.5) < 1e-12

    # the buffer protocol hands numpy a zero-copy view
    import numpy

    # so a numpy array over the vector
    array = numpy.asarray(vector)
    # has the same shape
    assert array.shape == (5,)
    # and writing through it
    array[0] = -1.0
    # changes the vector
    assert vector.get(0) == -1.0

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
