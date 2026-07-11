#!/usr/bin/env python3
# -*- Python -*-
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

    # a histogram of ten bins over [0, 10)
    h = libgsl.Histogram(bins=10)
    assert h.bins == 10 and len(h) == 10
    h.uniform(0, 10)
    assert h.sum == 0
    assert h.lower == 0 and h.upper == 10

    # accumulate a pattern, twice into bin four
    for x in [0.5, 1.5, 2.5, 3.5, 4.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]:
        h.increment(x)

    # the queries
    assert h.find(4.5) == 4
    assert h.find(-1) is None
    assert h[4] == 2
    assert h.max() == 2 and h.argmax() == 4
    assert h.min() == 1
    assert h.sum == 11

    # the {i}th bin range, and its bounds check
    assert h.range(4) == (4, 5)
    assert raises(lambda: h[10], IndexError)
    assert raises(lambda: h.range(10), IndexError)

    # the statistics are defined
    assert h.mean > 0 and h.sdev >= 0

    # a clone is independent
    c = h.clone()
    c.increment(4.5)
    assert c[4] == 3 and h[4] == 2

    # arithmetic operators, dispatched by type in the extension
    h *= 2
    assert h[4] == 4 and h.sum == 22
    h += h.clone()
    assert h[4] == 8

    # the buffer protocol hands numpy the counts
    import numpy

    counts = numpy.asarray(h)
    assert counts.shape == (10,)
    assert counts[4] == 8

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
