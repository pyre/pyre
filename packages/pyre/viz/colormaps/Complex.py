# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# support
import pyre

# the protocol
from .Colormap import Colormap


# a map well suited to rendering complex values
class Complex(
    pyre.flow.factory, family="pyre.viz.colormaps.complex", implements=Colormap
):
    """
    The HSB colormap
    """

    # the inputs
    signal = pyre.viz.tile.input()
    signal.doc = "the complex signal"

    # the outputs
    red = pyre.viz.tile.output()
    red.doc = "the red channel"

    green = pyre.viz.tile.output()
    green.doc = "the green channel"

    blue = pyre.viz.tile.output()
    blue.doc = "the blue channel"

    # user configurable state
    bins = pyre.properties.int(default=32)
    bins.doc = "the number of value quantization bins"

    amplitude = pyre.properties.tuple(schema=pyre.properties.float(), default=(0, 1))
    amplitude.doc = "the data space"

    brightness = pyre.properties.tuple(schema=pyre.properties.float(), default=(0, 1))
    brightness.doc = "the brightness range"

    underflow = pyre.properties.tuple(schema=pyre.properties.float(), default=(0, 0, 0))
    underflow.doc = "the color of underflow data"

    overflow = pyre.properties.tuple(schema=pyre.properties.float(), default=(1, 1, 1))
    overflow.doc = "the color of overflow data"


# end of file
