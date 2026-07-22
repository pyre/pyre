#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: verify that the grid package is accessible
"""


def test():
    # access the package
    import pyre.grid

    # the factory and the grid class are published when the bindings are present
    assert hasattr(pyre.grid, "heap")
    assert hasattr(pyre.grid, "grid")

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
