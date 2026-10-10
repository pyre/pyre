# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Image import Image


# a microsoft v2 BMP image
class BMP(pyre.flow.product, family="pyre.viz.images.bmp", implements=Image):
    """
    A microsoft v2 BMP image
    """


# end of file
