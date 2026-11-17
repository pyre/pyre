#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the bound {Histogram} directly, through the extension rather than the {gsl.histogram}
shim, so a failure isolates the c++ layer
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

    # make a histogram of ten bins
    h = libgsl.Histogram(bins=10)
    # which knows how many bins it has
    assert h.bins == 10 and len(h) == 10
    # spread them evenly over [0, 10)
    h.uniform(0, 10)
    # the histogram starts out empty
    assert h.sum == 0
    # and spans the interval it was given
    assert h.lower == 0 and h.upper == 10

    # accumulate a pattern that lands once in every bin, and once more in bin four
    for x in [0.5, 1.5, 2.5, 3.5, 4.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]:
        # by adding one count for each value
        h.increment(x)

    # a value falls in the bin that contains it
    assert h.find(4.5) == 4
    # and a value outside the range falls in none
    assert h.find(-1) is None
    # bin four holds two counts
    assert h[4] == 2
    # which is the largest count, in that bin
    assert h.max() == 2 and h.argmax() == 4
    # every other bin holds one
    assert h.min() == 1
    # and the counts add up to the number of values
    assert h.sum == 11

    # the {i}th bin covers its unit interval
    assert h.range(4) == (4, 5)
    # access past the last bin is refused
    assert raises(lambda: h[10], IndexError)
    # and so is asking for its range
    assert raises(lambda: h.range(10), IndexError)

    # the statistics are defined
    assert h.mean > 0 and h.sdev >= 0

    # make a clone
    c = h.clone()
    # add to it
    c.increment(4.5)
    # and check that the original did not change
    assert c[4] == 3 and h[4] == 2

    # the arithmetic operators are dispatched by type in the extension: scale by a number
    h *= 2
    # which scales every count
    assert h[4] == 4 and h.sum == 22
    # add another histogram
    h += h.clone()
    # which adds bin by bin
    assert h[4] == 8

    # the buffer protocol hands numpy the counts
    import numpy

    # as an array
    counts = numpy.asarray(h)
    # with one cell per bin
    assert counts.shape == (10,)
    # that holds the count of that bin
    assert counts[4] == 8

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
