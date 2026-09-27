#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
numpy imports a grid through dlpack without copying its cells
"""


def test():
    # support
    import numpy
    import pyre.grid

    # make a grid
    g = pyre.grid.heap(shape=(2, 3), cell="float64")
    # fill it
    numpy.asarray(g)[...] = numpy.arange(6).reshape(2, 3)
    # import it
    a = numpy.from_dlpack(g)
    # the import sees the cells of the grid
    assert a.ctypes.data == g.address
    # with their values
    assert (a == numpy.arange(6).reshape(2, 3)).all()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
