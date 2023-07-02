# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# base types
from .. import disktypes


# the memtype base class
class MemoryType:
    """
    A memory type specification
    """

    # constants
    ctype: str = "void"
    htype: disktypes.type = None

    # data
    @property
    def tag(self):
        """
        Generate my type tag
        """
        # use my class name as the tag; this is currently consistent with the {pyre.memory}
        # bindings, so it can be interpolated into class names when requesting specific
        # template instantiations
        return type(self).__name__

    # interface
    def heap(self, cells):
        """
        Allocate a memory buffer on the heap that can fit the given number of {cells} of my type
        """
        # build the name of the buffer factory
        name = f"{self.tag}Heap"
        # get the buffer factory
        allocator = getattr(pyre.libpyre.memory, name)
        # allocate the buffer and return it
        return allocator(cells=cells)

    def grid(self, shape):
        """
        Allocate a grid on the heap of the given {shape}
        """
        # get my type tag
        tag = self.tag
        # get the rank
        rank = len(shape)
        # build the name of the shape
        sname = f"Shape{rank}D"
        # the name of the packing
        cname = f"Canonical{rank}D"
        # the name of the storage
        mname = f"{tag}Heap"
        # and the name of the grid
        gname = f"{tag}HeapGrid{rank}D"

        # grab the binding
        libpyre = pyre.libpyre
        # build the shape
        shape = getattr(libpyre.grid, sname)(shape=shape)
        # use it to make the packing
        packing = getattr(libpyre.grid, cname)(shape=shape)
        # allocate storage
        storage = getattr(libpyre.memory, mname)(cells=shape.cells)
        # assemble the grid
        grid = getattr(libpyre.grid, gname)(packing=packing, storage=storage)
        # and return it
        return grid

    # metamethods
    def __str__(self):
        # use my {ctype} as my marker
        return self.ctype


# end of file
