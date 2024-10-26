# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# support
import pyre

# protocol
from .Codec import Codec


# a factory of microsoft BMP v2 rasters
class BMP(pyre.flow.factory, family="pyre.viz.codecs.bmp", implements=Codec):
    """
    A codec that encodes its {red}, {green} and {blue} channels into a
    microsoft v2 BMP bitmap
    """

    # the inputs
    red = pyre.viz.tile.input()
    red.doc = "the red channel"

    green = pyre.viz.tile.input()
    green.doc = "the green channel"

    blue = pyre.viz.tile.input()
    blue.doc = "the blue channel"

    # the output
    bmp = pyre.viz.raster.output()
    bmp.default = pyre.viz.rasters.bmp
    bmp.doc = "the BMP encoded signal"


# end of file
