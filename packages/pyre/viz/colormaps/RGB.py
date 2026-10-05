# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Colormap import Colormap


# the colormap that paints three signals into the three color channels
class RGB(pyre.flow.factory, family="pyre.viz.colormaps.rgb", implements=Colormap):
    """
    The colormap that paints three signals, each a stream of values in [0,1], into the red,
    green, and blue channels
    """

    # the inputs; their names differ from those of the outputs, since a factory names each of
    # its slots once
    redSource = pyre.viz.tile.input()
    redSource.doc = "the signal painted red"

    greenSource = pyre.viz.tile.input()
    greenSource.doc = "the signal painted green"

    blueSource = pyre.viz.tile.input()
    blueSource.doc = "the signal painted blue"

    # the outputs
    red = pyre.viz.tile.output()
    red.doc = "the red channel"
    green = pyre.viz.tile.output()
    green.doc = "the green channel"
    blue = pyre.viz.tile.output()
    blue.doc = "the blue channel"


# end of file
