#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A grid on host storage has no cuda array interface
"""


def test():
    # support
    import pyre.grid

    # make a grid on the heap
    g = pyre.grid.heap(shape=(2, 2), cell="float64")
    # the device cannot reach its cells, so it offers no interface
    assert not hasattr(g, "__cuda_array_interface__")

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
