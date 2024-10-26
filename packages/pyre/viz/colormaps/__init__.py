# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# support
import pyre

# the protocol
from .Colormap import Colormap as colormap


# the implementations
@pyre.foundry(implements=colormap, tip="the complex colormap")
def complex():
    """
    The complex colormap
    """
    # pull the implementation
    from .Complex import Complex

    # and publish it
    return Complex


@pyre.foundry(implements=colormap, tip="the gray scale colormap")
def gray():
    """
    The gray colormap
    """
    # pull the implementation
    from .Gray import Gray

    # and publish it
    return Gray


@pyre.foundry(implements=colormap, tip="the HSB colormap")
def hsb():
    """
    The HSB colormap
    """
    # pull the implementation
    from .HSB import HSB

    # and publish it
    return HSB


@pyre.foundry(implements=colormap, tip="the HSL colormap")
def hl():
    """
    The HL colormap
    """
    # pull the implementation
    from .HL import HL

    # and publish it
    return HL


@pyre.foundry(implements=colormap, tip="the HSL colormap")
def hsl():
    """
    The HSL colormap
    """
    # pull the implementation
    from .HSL import HSL

    # and publish it
    return HSL


# end of file
