# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# check whether the bindings exist and support the basic cell types
try:
    # build the predicate
    cells = pyre.libpyre.memory.cells if pyre.libpyre else None
# if the bindings exist but don't have cell support
except AttributeError:
    # mark
    cells = None

# if there support
if cells:
    # publish
    # the sentinel
    cell = cells.Cell

    # signed integral types
    int8 = cells.Int8
    int16 = cells.Int16
    int32 = cells.Int32
    int64 = cells.Int64
    # unsigned integral types
    uint8 = cells.UInt8
    uint16 = cells.UInt16
    uint32 = cells.UInt32
    uint64 = cells.UInt64
    # floats
    float = cells.Float
    double = cells.Double
    # complex
    complexFloat = cells.ComplexFloat
    complexDouble = cells.ComplexDouble

    # const versions
    # signed integral types
    int8Const = cells.Int8Const
    int16Const = cells.Int16Const
    int32Const = cells.Int32Const
    int64Const = cells.Int64Const
    # unsigned integral types
    uint8Const = cells.UInt8Const
    uint16Const = cells.UInt16Const
    uint32Const = cells.UInt32Const
    uint64Const = cells.UInt64Const
    # floats
    floatConst = cells.FloatConst
    doubleConst = cells.DoubleConst
    # complex
    complexFloatConst = cells.ComplexFloatConst
    complexDoubleConst = cells.ComplexDoubleConst

    # cells in an explicit byte order; the spelling that matches the host's order is the native
    # cell itself, the other one swaps bytes on every access
    # big endian
    # signed integral types
    int16BE = cells.Int16BE
    int32BE = cells.Int32BE
    int64BE = cells.Int64BE
    # unsigned integral types
    uint16BE = cells.UInt16BE
    uint32BE = cells.UInt32BE
    uint64BE = cells.UInt64BE
    # floats
    floatBE = cells.FloatBE
    doubleBE = cells.DoubleBE
    # complex
    complexFloatBE = cells.ComplexFloatBE
    complexDoubleBE = cells.ComplexDoubleBE
    # const versions
    # signed integral types
    int16BEConst = cells.Int16BEConst
    int32BEConst = cells.Int32BEConst
    int64BEConst = cells.Int64BEConst
    # unsigned integral types
    uint16BEConst = cells.UInt16BEConst
    uint32BEConst = cells.UInt32BEConst
    uint64BEConst = cells.UInt64BEConst
    # floats
    floatBEConst = cells.FloatBEConst
    doubleBEConst = cells.DoubleBEConst
    # complex
    complexFloatBEConst = cells.ComplexFloatBEConst
    complexDoubleBEConst = cells.ComplexDoubleBEConst

    # little endian
    # signed integral types
    int16LE = cells.Int16LE
    int32LE = cells.Int32LE
    int64LE = cells.Int64LE
    # unsigned integral types
    uint16LE = cells.UInt16LE
    uint32LE = cells.UInt32LE
    uint64LE = cells.UInt64LE
    # floats
    floatLE = cells.FloatLE
    doubleLE = cells.DoubleLE
    # complex
    complexFloatLE = cells.ComplexFloatLE
    complexDoubleLE = cells.ComplexDoubleLE
    # const versions
    # signed integral types
    int16LEConst = cells.Int16LEConst
    int32LEConst = cells.Int32LEConst
    int64LEConst = cells.Int64LEConst
    # unsigned integral types
    uint16LEConst = cells.UInt16LEConst
    uint32LEConst = cells.UInt32LEConst
    uint64LEConst = cells.UInt64LEConst
    # floats
    floatLEConst = cells.FloatLEConst
    doubleLEConst = cells.DoubleLEConst
    # complex
    complexFloatLEConst = cells.ComplexFloatLEConst
    complexDoubleLEConst = cells.ComplexDoubleLEConst


# end of file
