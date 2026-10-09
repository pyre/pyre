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


# the OKLCH colormap
class OKLCH(pyre.flow.factory, family="pyre.viz.colormaps.oklch", implements=Colormap):
    """
    The colormap that paints perceptual lightness, chroma, and hue into the three color channels;
    equal steps in its inputs look like equal steps in color
    """

    # the inputs
    lightness = pyre.viz.tile.input()
    lightness.doc = "the perceptual lightness, in [0,1]"

    chroma = pyre.viz.tile.input()
    chroma.doc = "the chroma, the colorfulness, in [0,1]"

    hue = pyre.viz.tile.input()
    hue.doc = "the hue, in degrees"

    # the outputs
    red = Channel.output()
    red.doc = "the red channel"

    green = Channel.output()
    green.doc = "the green channel"

    blue = Channel.output()
    blue.doc = "the blue channel"


# end of file
