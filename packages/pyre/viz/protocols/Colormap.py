# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the specifications of my slots
from .Channel import Channel


# the protocol for all color maps
class Colormap(pyre.flow.producer, family="pyre.viz.colormaps"):
    """
    The colormap protocol; the inputs depend on the colormap, the three color channels are
    common to all
    """

    # the outputs
    red = Channel.output()
    red.doc = "the red channel"

    green = Channel.output()
    green.doc = "the green channel"

    blue = Channel.output()
    blue.doc = "the blue channel"


# end of file
