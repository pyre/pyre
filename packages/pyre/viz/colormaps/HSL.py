# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# support
import pyre

# the protocol
from .Colormap import Colormap


# the HSL color map
class HSL(pyre.flow.factory, family="pyre.viz.colormaps.hsl", implements=Colormap):
    """
    The HSL colormap
    """

    # the inputs
    hue = pyre.viz.tile.input()
    hue.doc = "the hue channel"

    saturation = pyre.viz.tile.input()
    saturation.doc = "the saturation channel"

    luminosity = pyre.viz.tile.input()
    luminosity.doc = "the luminosity channel"

    # the outputs
    red = pyre.viz.tile.output()
    red.doc = "the red channel"

    green = pyre.viz.tile.output()
    green.doc = "the green channel"

    blue = pyre.viz.tile.output()
    blue.doc = "the blue channel"


# end of file
