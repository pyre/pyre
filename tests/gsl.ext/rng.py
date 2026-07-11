#!/usr/bin/env python3
# -*- Python -*-
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

    # the catalogue of generators is a non-empty set of names
    available = libgsl.rng_avail()
    assert isinstance(available, (set, frozenset))
    assert "taus" in available

    # build a named generator and seed it
    r = libgsl.RNG(algorithm="taus")
    assert r.algorithm == "taus"
    # seeding returns the generator, for chaining
    assert r.seed(42) is r

    # its range is a pair, low below high
    low, high = r.range
    assert low < high

    # a draw from the unit interval stays in [0, 1)
    x = r.float()
    assert 0.0 <= x < 1.0

    # a draw of an integer lands within the range
    n = r.int()
    assert low <= n <= high

    # an unknown algorithm is rejected
    try:
        # ask for a generator that does not exist
        libgsl.RNG(algorithm="no-such-generator")
    # which is what should happen
    except ValueError:
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
