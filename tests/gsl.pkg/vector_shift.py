#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise adding a constant to every vector element
"""


def test():
    # package access
    import gsl

    # make a vector and initialize it
    v = gsl.vector(shape=100).fill(value=1)
    # check
    for e in v:
        assert e == 1
    # shift it
    v += 1
    # check
    for e in v:
        assert e == 2
    # all done
    return v


# main
if __name__ == "__main__":
    test()


# end of file
