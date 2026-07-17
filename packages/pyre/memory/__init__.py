# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre
import journal

# publish
from . import cells


# memory buffers
# on the heap
def heap(type: cells.cell, cells: int):
    """
    Allocate a buffer of the given number of {cells} of the given {type}
    """
    # if the {type} is const
    if not type.mutable:
        # these are of very limited value
        channel = journal.warning("pyre.memory.heap")
        # report
        channel.line(f"read-only buffers on the heap are of limited value")
        channel.line("while allocating a memory block on the heap")
        channel.line(f"with {cells} cells of type 'const {type.declValue}'")
        # flush
        channel.log()

    # get the module with the heap factories
    module = pyre.libpyre.memory.heaps
    # look up the factory
    heapFactory = getattr(module, f"Heap{type.__class__.__name__}")
    # allocate
    heap = heapFactory(cells=cells)
    # and return it
    return heap


# file backed
def map(uri: pyre.primitives.path, type: cells.cell, cells: int = 0):
    """
    Allocate a file backed buffer
    """
    # get the module with the map factories
    module = pyre.libpyre.memory.maps
    # look up the factory
    mapFactory = getattr(module, f"Map{type.__class__.__name__}")
    # if the {type} is mutable and i know how many {cells} to allocate
    if type.mutable and cells > 0:
        # allocate and return
        return mapFactory(uri=str(uri), cells=cells)
    # if the {type} is immutable:
    if not type.mutable:
        # allocate and return
        return mapFactory(uri=str(uri))

    # anything else is an error; make a channel
    channel = journal.error("pyre.memory.map")
    # complain
    channel.line("unsupported request for a memory mapped buffer")
    # and flush
    channel.log()

    # just in case errors aren't fatal
    return


# end of file
