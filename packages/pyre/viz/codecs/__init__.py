# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# support
import pyre

# the protocol
from .Codec import Codec as codec


# the implementations
@pyre.foundry(implements=codec, tip="an encoder that produces microsoft v2 BMP rasters")
def bmp():
    """ """
    # pull the implementation
    from .BMP import BMP

    # and publish it
    return BMP


# end of file
