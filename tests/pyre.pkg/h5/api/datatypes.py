#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the bound datatypes support equality comparison
"""


def test():
    # get the package
    import pyre.h5

    # the on-disk native datatypes
    disktypes = pyre.h5.disktypes

    # a datatype compares equal to itself
    assert disktypes.float == disktypes.float
    assert disktypes.double == disktypes.double
    assert disktypes.int32 == disktypes.int32

    # and unequal to a different datatype
    assert disktypes.float != disktypes.double
    assert disktypes.int32 != disktypes.int64
    assert not (disktypes.float == disktypes.int32)

    # equality is by datatype, not object identity: an independent copy still compares equal
    from pyre.extensions import libh5

    other = libh5.types.float(disktypes.float)
    assert other is not disktypes.float
    assert other == disktypes.float

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
