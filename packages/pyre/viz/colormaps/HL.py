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


# the HL color map
class HL(pyre.flow.factory, family="pyre.viz.colormaps.hl", implements=Colormap):
    """
    The HL colormap
    """

    # user configurable state
    threshold = pyre.properties.float()
    threshold.default = 0.4
    threshold.doc = "the floor each color fades to as the hue moves away from it"

    # the inputs
    hue = pyre.viz.tile.input()
    hue.doc = "the hue channel"

    luminosity = pyre.viz.tile.input()
    luminosity.doc = "the luminosity channel"

    # the outputs
    red = Channel.output()
    red.doc = "the red channel"

    green = Channel.output()
    green.doc = "the green channel"

    blue = Channel.output()
    blue.doc = "the blue channel"

    # the c++ templates whose instantiations do my work, when a recipe is staged
    pyre_engines = ("pyre::viz::factories::colormaps::hl_t",)


# end of file
