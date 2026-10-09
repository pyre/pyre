# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Colormap import Colormap

# the specification of my outputs
from ..protocols.Channel import Channel


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
    red = Channel.output()
    red.doc = "the red channel"

    green = Channel.output()
    green.doc = "the green channel"

    blue = Channel.output()
    blue.doc = "the blue channel"


# end of file
