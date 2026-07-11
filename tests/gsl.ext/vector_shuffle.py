#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the bound {Vector.shuffle} directly, through the extension rather than the {gsl.vector}
shim, so a failure isolates the c++ layer
"""


def test():
    # the bindings
    from gsl import libgsl

    # a vector of distinct values
    v = libgsl.Vector(shape=6)
    for index in range(6):
        v.set(index, float(index))

    # a seeded generator makes the shuffle reproducible
    rng = libgsl.RNG("mt19937").seed(42)

    # shuffle in place
    v.shuffle(rng)

    # the permutation is pinned to the mt19937 stream
    assert v.tuple() == (5.0, 1.0, 0.0, 4.0, 3.0, 2.0)
    # and no value is gained or lost
    assert sorted(v.tuple()) == [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
