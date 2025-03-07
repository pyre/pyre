# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import pyre

# get the bindings
cells = pyre.libpyre.memory.cells

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


# end of file
