#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Managed grids and host grids combine where the device can reach the cells, and only there
"""


def test():
    # support
    import numpy
    import pyre.cuda
    import pyre.grid

    # a managed grid
    m = pyre.cuda.managed(shape=(4,), cell="float64")
    # and a host one
    h = pyre.grid.heap(shape=(4,), cell="float64")
    # filled with known values
    numpy.asarray(m)[...] = 2
    numpy.asarray(h)[...] = 1
    # work queued on the device
    m *= 3.0
    # a host grid takes a managed one, after waiting for the device
    h += m
    assert (numpy.asarray(h) == 7).all()
    # but the device cannot reach the cells of a host grid
    try:
        # so this
        m += h
    # is refused
    except TypeError:
        # as it should be
        pass
    # and anything else is a bug
    else:
        # so say so
        assert False, "a managed grid took the cells of a host grid"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
