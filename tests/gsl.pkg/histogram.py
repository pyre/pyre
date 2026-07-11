#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the gsl histogram: allocation, binning, accumulation, statistics, and arithmetic
"""


def test():
    # get the package
    import gsl

    # make a histogram of ten bins
    h = gsl.histogram(bins=10)
    # the extension knows how many bins it holds
    assert len(h) == 10
    assert h.bins == 10

    # lay the bins out uniformly over [0, 10), which also zeroes them
    h.uniform(lower=0, upper=10)
    # so it starts empty
    assert h.sum == 0
    # over the range we asked for
    assert h.lower == 0
    assert h.upper == 10

    # drop a value into each bin, twice into the fifth, filling from a run of samples
    h.fill([0.5, 1.5, 2.5, 3.5, 4.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5])

    # the value 4.5 lands in bin four
    assert h.find(4.5) == 4
    # a value outside the range lands in no bin at all
    assert h.find(-1) is None
    # bin four now holds two counts, the most of any bin
    assert h[4] == 2
    assert h.max() == 2
    assert h.argmax() == 4
    # the least populated bins hold one
    assert h.min() == 1
    # and the total is the eleven values we dropped in
    assert h.sum == 11

    # the fourth bin covers [4, 5)
    lower, upper = h.range(4)
    assert lower == 4 and upper == 5

    # the statistics are defined
    assert h.mean > 0
    assert h.sdev >= 0

    # reading past the end raises, rather than reading garbage
    try:
        # ask for a bin that does not exist
        h[10]
    # which is what should happen
    except IndexError:
        pass
    # and if it doesn't
    else:
        # the guard is gone
        assert False, "an out of range bin should not be readable"

    # a clone carries the same counts, in independent storage
    c = h.clone()
    assert c is not h
    assert c.sum == h.sum
    assert c[4] == h[4]

    # incrementing the clone leaves the original untouched
    c.increment(4.5)
    assert c[4] == 3
    assert h[4] == 2

    # the counts come back as a vector
    v = h.counts()
    assert v.shape == 10
    assert v[4] == 2

    # numpy reads the counts through the buffer protocol, without copying
    import numpy

    counts = numpy.asarray(h)
    assert counts.shape == (10,)
    assert counts[4] == 2

    # scaling doubles every count
    h *= 2
    assert h[4] == 4
    assert h.sum == 22

    # adding a histogram to itself folds its counts in bin by bin
    h += h.clone()
    assert h[4] == 8

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
