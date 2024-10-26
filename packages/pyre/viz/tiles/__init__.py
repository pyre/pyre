# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# support
import pyre

# the protocol
from .Tile import Tile as tile


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
