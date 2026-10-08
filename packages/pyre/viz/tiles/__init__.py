# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Tile import Tile as tile

# its refinements, by what the cells hold
from ..protocols.Complex import Complex as complex
from ..protocols.Real import Real as real
from ..protocols.Magnitude import Magnitude as magnitude
from ..protocols.Unit import Unit as unit
from ..protocols.Channel import Channel as channel


# the implementations
@pyre.foundry(implements=tile, tip="a tile with dynamically allocated memory")
def heap():
    """ """
    # pull the implementation
    from .Heap import Heap

    # and publish it
    return Heap


@pyre.foundry(implements=tile, tip="a tile with memory from a memory mapped file")
def map():
    """ """
    # pull the implementation
    from .Map import Map

    # and publish it
    return Map


@pyre.foundry(implements=tile, tip="a tile with borrowed memory")
def view():
    """ """
    # pull the implementation
    from .View import View

    # and publish it
    return View


# end of file
