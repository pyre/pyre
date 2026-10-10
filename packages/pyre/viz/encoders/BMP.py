# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# protocol
from ..protocols.Encoder import Encoder

# the specifications of my slots
from ..protocols.Channel import Channel


# a factory of microsoft BMP v2 images
class BMP(pyre.flow.factory, family="pyre.viz.encoders.bmp", implements=Encoder):
    """
    An encoder that encodes its {red}, {green} and {blue} channels into a
    microsoft v2 BMP bitmap
    """

    # the inputs
    red = Channel.input()
    red.doc = "the red channel"

    green = Channel.input()
    green.doc = "the green channel"

    blue = Channel.input()
    blue.doc = "the blue channel"

    # the output
    image = pyre.viz.image.output()
    image.default = pyre.viz.images.bmp
    image.doc = "the BMP encoded signal"

    # the c++ templates whose instantiations do my work, when a recipe is staged
    pyre_engines = ("pyre::viz::factories::codecs::bmp_t",)


# end of file
