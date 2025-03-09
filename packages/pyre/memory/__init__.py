# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import pyre

# publish
from . import cells


# convenience
def heap(cells: int, type: cells.cell):
    """
    Allocate a buffer of the given number of {cells} of the given {type}
    """
    # get the module with the heap factories
    module = pyre.libpyre.memory.heaps
    # look up the factory
    factory = getattr(module, f"Heap{type.__class__.__name__}")
    # allocate
    heap = factory(cells=cells)
    # and return it
    return heap


# end of file
