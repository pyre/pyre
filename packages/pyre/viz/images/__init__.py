# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Image import Image as image


# the implementations
@pyre.foundry(implements=image, tip="a microsoft v2 BMP image")
def bmp():
    """ """
    # pull the implementation
    from .BMP import BMP

    # and publish it
    return BMP


# end of file
