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
int8Const = cells.ConstInt8
int16Const = cells.ConstInt16
int32Const = cells.ConstInt32
int64Const = cells.ConstInt64
# unsigned integral types
uint8Const = cells.ConstUInt8
uint16Const = cells.ConstUInt16
uint32Const = cells.ConstUInt32
uint64Const = cells.ConstUInt64
# floats
floatConst = cells.ConstFloat
doubleConst = cells.ConstDouble
# complex
complexFloatConst = cells.ConstComplexFloat
complexDoubleConst = cells.ConstComplexDouble


# end of file
