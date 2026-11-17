#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the bound {RNG} directly, through the extension rather than the {gsl.rng} shim, so a
failure isolates the c++ layer
"""


def test():
    # the bindings
    from gsl import libgsl

    # get the catalogue of generators
    available = libgsl.rng_avail()
    # which is a set of names
    assert isinstance(available, (set, frozenset))
    # that includes a well known one
    assert "taus" in available

    # build a named generator
    r = libgsl.RNG(algorithm="taus")
    # that knows its name
    assert r.algorithm == "taus"
    # seeding returns the generator, for chaining
    assert r.seed(42) is r

    # its range is a pair
    low, high = r.range
    # with the low end below the high one
    assert low < high

    # draw from the unit interval
    x = r.float()
    # and check that the draw stays in [0, 1)
    assert 0.0 <= x < 1.0

    # draw an integer
    n = r.int()
    # and check that it lands within the range
    assert low <= n <= high

    # an unknown algorithm is rejected
    try:
        # ask for a generator that does not exist
        libgsl.RNG(algorithm="no-such-generator")
    # which is what should happen
    except ValueError:
        # so there is nothing else to check
        pass
    # and if it doesn't
    else:
        # the guard is gone
        assert False, "an unknown algorithm should be rejected"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
