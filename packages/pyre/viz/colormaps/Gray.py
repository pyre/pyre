# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# support
import pyre

# the protocol
from .Colormap import Colormap


# the gray colormap
class Gray(pyre.flow.factory, family="pyre.viz.colormaps.gray", implements=Colormap):
    """
    The colormap that turns a stream of values in [0,1] into gray scale
    """

    # the input
    signal = pyre.viz.tile.input()
    signal.doc = "the input signal, a stream of values in [0,1]"

    # the outputs
    red = pyre.viz.tile.output()
    red.doc = "the red channel"

    green = pyre.viz.tile.output()
    green.doc = "the green channel"

    blue = pyre.viz.tile.output()
    blue.doc = "the blue channel"


# end of file
