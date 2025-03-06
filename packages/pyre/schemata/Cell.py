# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# the framework
import pyre

# superclass
from .Schema import Schema


# declaration
class Cell(Schema):
    """
    A type declarator for types
    """

    # constants
    typename = "cell"  # the name of my type
    complaint = "could not coerce {0.value!r} to cell"

    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} into a cell
        """
        # actual cells
        if isinstance(value, pyre.memory.cells.cell):
            # pass through unchanged
            return value
        # strings
        if isinstance(value, str):
            # if i don't have a translation table yet
            if self.xlat is None:
                # build it as a class resource
                Cell.xlat = self.makeTranslationTable()
            # carefully
            try:
                # attempt the conversion
                return Cell.xlat[value.lower()]
            # lookup failures
            except Exception as error:
                # get reported as casting errors
                raise self.CastingError(description=self.complaint, value=value)
        # all other types are incompatible, for now
        raise self.CastingError(description=self.complaint, value=value)

    # meta-methods
    def __init__(self, default=True, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return

    # implementation details
    # the name lookup table
    @classmethod
    def makeTranslationTable(cls):
        """
        Build the translation table from type aliases to actual cells
        """
        # build the table
        xlat = {
            # mutable types
            # bytes
            "c": pyre.memory.cells.uint8,
            "char": pyre.memory.cells.uint8,
            # signed integers
            "i1": pyre.memory.cells.int8,
            "int8": pyre.memory.cells.int8,
            "i2": pyre.memory.cells.int16,
            "int16": pyre.memory.cells.int16,
            "i4": pyre.memory.cells.int32,
            "int32": pyre.memory.cells.int32,
            "i8": pyre.memory.cells.int64,
            "int64": pyre.memory.cells.int64,
            # unsigned integers
            "u1": pyre.memory.cells.uint8,
            "uint8": pyre.memory.cells.uint8,
            "u2": pyre.memory.cells.uint16,
            "uint16": pyre.memory.cells.uint16,
            "u4": pyre.memory.cells.uint32,
            "uint32": pyre.memory.cells.uint32,
            "u8": pyre.memory.cells.uint64,
            "uint64": pyre.memory.cells.uint64,
            # floats
            "r4": pyre.memory.cells.float,
            "real32": pyre.memory.cells.float,
            "float32": pyre.memory.cells.float,
            "r8": pyre.memory.cells.double,
            "real64": pyre.memory.cells.double,
            "float64": pyre.memory.cells.double,
            # complex
            "c8": pyre.memory.cells.complexFloat,
            "complex64": pyre.memory.cells.complexFloat,
            "c16": pyre.memory.cells.complexDouble,
            "complex128": pyre.memory.cells.complexDouble,
            # const types
            # bytes
            "const c": pyre.memory.cells.uint8Const,
            "const char": pyre.memory.cells.uint8Const,
            # signed integers
            "const i1": pyre.memory.cells.int8Const,
            "const int8": pyre.memory.cells.int8Const,
            "const i2": pyre.memory.cells.int16Const,
            "const int16": pyre.memory.cells.int16Const,
            "const i4": pyre.memory.cells.int32Const,
            "const int32": pyre.memory.cells.int32Const,
            "const i8": pyre.memory.cells.int64Const,
            "const int64": pyre.memory.cells.int64Const,
            # unsigned integers
            "const u1": pyre.memory.cells.uint8Const,
            "const uint8": pyre.memory.cells.uint8Const,
            "const u2": pyre.memory.cells.uint16Const,
            "const uint16": pyre.memory.cells.uint16Const,
            "const u4": pyre.memory.cells.uint32Const,
            "const uint32": pyre.memory.cells.uint32Const,
            "const u8": pyre.memory.cells.uint64Const,
            "const uint64": pyre.memory.cells.uint64Const,
            # floats
            "const r4": pyre.memory.cells.floatConst,
            "const real32": pyre.memory.cells.floatConst,
            "const float32": pyre.memory.cells.floatConst,
            "const r8": pyre.memory.cells.doubleConst,
            "const real64": pyre.memory.cells.doubleConst,
            "const float64": pyre.memory.cells.doubleConst,
            # complex
            "const c8": pyre.memory.cells.complexFloatConst,
            "const complex64": pyre.memory.cells.complexFloatConst,
            "const c16": pyre.memory.cells.complexDoubleConst,
            "const complex128": pyre.memory.cells.complexDoubleConst,
        }
        # and return it
        return xlat

    # the table placeholder
    xlat = None


# end of file
