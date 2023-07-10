# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# get the bindings
from .. import libh5


# the base type
type = libh5.datatypes.DataType

# abstract types; useful as building blocks while defining new types
from .Array import Array as arrayType
from .Compound import Compound as compoundType
from .Enum import Enum as enumType
from .Float import Float as floatType
from .Integer import Integer as intType
from .String import String as strType

# alias the type categories to provide access to more esoteric types
native = libh5.datatypes.native
big = libh5.datatypes.big
little = libh5.datatypes.little
std = libh5.datatypes.std
alpha = libh5.datatypes.alpha
ieee = libh5.datatypes.ieee
intel = libh5.datatypes.intel
mips = libh5.datatypes.mips

# concrete types - native
# explicitly sized integral
int8 = native.int8
int16 = native.int16
int32 = native.int32
int64 = native.int64
uint8 = native.uint8
uint16 = native.uint16
uint32 = native.uint32
uint64 = native.uint64
# implicitly sized integral
char = native.char
signedChar = native.signedChar
unsignedChar = native.unsignedChar
short = native.short
unsignedShort = native.unsignedShort
int = native.int
unsignedInt = native.unsignedInt
long = native.long
unsignedLong = native.unsignedLong
longlong = native.longlong
unsignedLongLong = native.unsignedLongLong

# floating point
half = native.half
float = native.float
double = native.double
complexHalf = native.complexHalf
complexFloat = native.complexFloat
complexDouble = native.complexDouble
# sized aliases
r16 = half
r32 = float
r64 = double
c32 = complexHalf
c64 = complexFloat
c128 = complexDouble

# numpy names
float16 = half
float32 = float
float64 = double
complex32 = complexHalf
complex64 = complexFloat
complex128 = complexDouble

# standard types - strings
c_s1 = std.c_s1
fortran_s1 = std.fortran_s1

# end of file
