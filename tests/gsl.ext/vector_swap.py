#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the bound {Vector.swap} directly, through the extension rather than the {gsl.vector}
shim, so a failure isolates the c++ layer
"""


def test():
    # the bindings
    from gsl import libgsl

    # an asymmetric vector, so the swap is visible
    v = libgsl.Vector(shape=4)
    for index, value in enumerate((3, 1, 4, 2)):
        v.set(index, float(value))

    # swap the first cell with the last, naming the last with a reflected negative index
    v.swap(0, -1)

    # only those two cells move
    assert v.tuple() == (2.0, 1.0, 4.0, 3.0)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
