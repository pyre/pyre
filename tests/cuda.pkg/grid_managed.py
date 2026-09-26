#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A managed grid is a grid of the cuda package, over managed storage
"""


def test():
    # support
    import pyre.cuda
    import pyre.grid

    # make a grid on managed memory
    g = pyre.cuda.managed(shape=(3, 4), cell="float64")
    # it is an instance of the grid class of the package
    assert isinstance(g, pyre.cuda.grid)
    # which is not the grid class of the host
    assert not isinstance(g, pyre.grid.grid)
    # its cells live in managed memory
    assert g.strategy == "managed"
    # with the shape we asked for
    assert g.shape == [3, 4]

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
