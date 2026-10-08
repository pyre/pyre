# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Colormap import Colormap

# the specifications of my slots
from ..protocols.Unit import Unit
from ..protocols.Channel import Channel


# the gray colormap
class Gray(pyre.flow.factory, family="pyre.viz.colormaps.gray", implements=Colormap):
    """
    The colormap that turns a stream of values in [0,1] into gray scale
    """

    # the input
    data = Unit.input()
    data.doc = "the input signal, a stream of values in [0,1]"

    # the outputs
    red = Channel.output()
    red.doc = "the red channel"

    green = Channel.output()
    green.doc = "the green channel"

    blue = Channel.output()
    blue.doc = "the blue channel"


# end of file
