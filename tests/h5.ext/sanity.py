#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that the {libh5} bindings are importable and carry the mosaic machinery
    """
    # get the bindings
    from pyre.extensions import libh5

    # the module-local flavors of the type-erased classes are registered
    assert hasattr(libh5, "Mosaic")
    assert hasattr(libh5, "Grid")
    # and datasets know how to make mosaics
    assert hasattr(libh5.DataSet, "mosaic")

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
