# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre
import journal

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

    # the cell types the grid factory understands, keyed by memtype tag
    _cells = {
        # signed integers, under all their spellings
        "Int8": "int8",
        "SignedChar": "int8",
        "Char": "int8",
        "Int16": "int16",
        "Short": "int16",
        "Int32": "int32",
        "Int": "int32",
        "Int64": "int64",
        "Long": "int64",
        # unsigned integers
        "UInt8": "uint8",
        "UnsignedChar": "uint8",
        "UInt16": "uint16",
        "UnsignedShort": "uint16",
        "UInt32": "uint32",
        "UnsignedInt": "uint32",
        "UInt64": "uint64",
        "UnsignedLong": "uint64",
        # floating point
        "Float": "float32",
        "Double": "float64",
        # complex
        "ComplexFloat": "complex64",
        "ComplexDouble": "complex128",
    }

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
        Allocate a grid on the heap of the given {shape}, over a fresh block of my cell type
        """
        # look up the cell type the grid factory understands
        cell = self._cells.get(self.tag)
        # if there is no grid support for my cell type
        if cell is None:
            # make a channel
            channel = journal.error("pyre.h5.memtypes")
            # complain
            channel.line(f"no grid support for the '{self.tag}' cell type")
            # flush
            channel.log()
            # and bail, just in case errors aren't fatal
            return None
        # the grid bindings expose a single type-erased grid class that presents the buffer protocol,
        # built here over a fresh block of heap memory of the right shape and cell type
        return pyre.libpyre.grid.heap(shape=list(shape), cell=cell)

    # metamethods
    def __str__(self):
        # use my {ctype} as my marker
        return self.ctype


# end of file
