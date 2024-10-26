# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# support
import pyre

# the protocol
from .Colormap import Colormap


# the HSB colormap
class HSB(pyre.flow.factory, family="pyre.viz.colormaps.hsb", implements=Colormap):
    """
    The HSB colormap
    """

    # the inputs
    hue = pyre.viz.tile.input()
    hue.doc = "the hue channel"

    saturation = pyre.viz.tile.input()
    saturation.doc = "the saturation channel"

    brightness = pyre.viz.tile.input()
    brightness.doc = "the brightness channel"

    # the outputs
    red = pyre.viz.tile.output()
    red.doc = "the red channel"

    green = pyre.viz.tile.output()
    green.doc = "the green channel"

    blue = pyre.viz.tile.output()
    blue.doc = "the blue channel"


# end of file
