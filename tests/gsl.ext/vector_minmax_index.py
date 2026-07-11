#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the bound {Vector.minIndex} and {Vector.maxIndex} directly, through the extension rather
than the {gsl.vector} shim, so a failure isolates the c++ layer
"""


def test():
    # the bindings
    from gsl import libgsl

    # a vector with a unique min and a unique max at distinct cells
    v = libgsl.Vector(shape=5)
    for index, value in enumerate((3, 1, 4, 0, 5)):
        v.set(index, float(value))

    # the smallest cell is the zero at index 3
    assert v.minIndex() == 3
    # the largest cell is the five at index 4
    assert v.maxIndex() == 4

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
