#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that the bound datatypes support equality comparison
    """
    # get the package
    import pyre.h5

    # the on-disk native datatypes
    disktypes = pyre.h5.disktypes

    # a datatype compares equal to itself: single precision floats
    assert disktypes.float == disktypes.float
    # double precision floats
    assert disktypes.double == disktypes.double
    # and integers
    assert disktypes.int32 == disktypes.int32

    # and unequal to a different datatype: floats of different precision
    assert disktypes.float != disktypes.double
    # integers of different widths
    assert disktypes.int32 != disktypes.int64
    # and a float and an integer of the same width
    assert not (disktypes.float == disktypes.int32)

    # equality is by datatype, not object identity
    from pyre.extensions import libh5

    # so make an independent copy
    other = libh5.types.float(disktypes.float)
    # which is a distinct object
    assert other is not disktypes.float
    # that still compares equal
    assert other == disktypes.float

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
