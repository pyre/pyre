#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Shuffle a vector into a random order, preserving the multiset of its values
"""


def test():
    # get the package
    import gsl

    # a vector of distinct values
    v = gsl.vector(shape=6)
    for index in range(6):
        v[index] = float(index)

    # a seeded generator makes the shuffle reproducible
    rng = gsl.rng(algorithm="mt19937")
    rng.seed(42)

    # shuffle in place
    v.shuffle(rng)

    # the permutation is pinned to the mt19937 stream
    assert v.tuple() == (5.0, 1.0, 0.0, 4.0, 3.0, 2.0)
    # and no value is gained or lost
    assert sorted(v.tuple()) == [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]

    # all done
    return v


# main
if __name__ == "__main__":
    test()


# end of file
