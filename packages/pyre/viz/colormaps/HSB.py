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
    red = Channel.output()
    red.doc = "the red channel"

    green = Channel.output()
    green.doc = "the green channel"

    blue = Channel.output()
    blue.doc = "the blue channel"

    # the c++ templates whose instantiations do my work, when a recipe is staged
    pyre_engines = ("pyre::viz::factories::colormaps::hsb_t",)


# end of file
