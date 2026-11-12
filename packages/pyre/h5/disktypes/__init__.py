# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# get the bindings
from .. import libh5

# the base type
type = libh5.types.datatype

# abstract types; useful as building blocks while defining new types
from .Array import Array as arrayType
from .Compound import Compound as compoundType
from .Enum import Enum as enumType
from .Float import Float as floatType
from .Integer import Integer as intType
from .String import String as strType

# alias the type categories to provide access to more esoteric types
native = libh5.types.native  # the types of this host
big = libh5.types.big  # the types stored in big endian order
little = libh5.types.little  # the types stored in little endian order
std = libh5.types.std  # the standard types
alpha = libh5.types.alpha  # the types of the dec alpha
ieee = libh5.types.ieee  # the ieee floating point types
intel = libh5.types.intel  # the types of intel processors
mips = libh5.types.mips  # the types of mips processors

# concrete types - native
# explicitly sized integral
int8 = native.int8  # a signed 8-bit integer
int16 = native.int16  # a signed 16-bit integer
int32 = native.int32  # a signed 32-bit integer
int64 = native.int64  # a signed 64-bit integer
uint8 = native.uint8  # an unsigned 8-bit integer
uint16 = native.uint16  # an unsigned 16-bit integer
uint32 = native.uint32  # an unsigned 32-bit integer
uint64 = native.uint64  # an unsigned 64-bit integer
# implicitly sized integral
char = native.char  # a {char}
signedChar = native.signedChar  # a {signed char}
unsignedChar = native.unsignedChar  # an {unsigned char}
short = native.short  # a {short}
unsignedShort = native.unsignedShort  # an {unsigned short}
int = native.int  # an {int}
unsignedInt = native.unsignedInt  # an {unsigned int}
long = native.long  # a {long}
unsignedLong = native.unsignedLong  # an {unsigned long}
longlong = native.longlong  # a {long long}
unsignedLongLong = native.unsignedLongLong  # an {unsigned long long}

# floating point
half = native.half  # a 16-bit float
float = native.float  # a 32-bit float
double = native.double  # a 64-bit float
# sized aliases
r16 = half  # the 16-bit float
r32 = float  # the 32-bit float
r64 = double  # the 64-bit float

# complex numbers
complexHalf = native.complexHalf  # two 16-bit floats
complexFloat = native.complexFloat  # two 32-bit floats
complexDouble = native.complexDouble  # two 64-bit floats

# radar samples: a pair of counts of each integer type
iqInt8 = native.iqInt8  # two signed 8-bit counts
iqInt16 = native.iqInt16  # two signed 16-bit counts
iqInt32 = native.iqInt32  # two signed 32-bit counts
iqInt64 = native.iqInt64  # two signed 64-bit counts
iqUInt8 = native.iqUInt8  # two unsigned 8-bit counts
iqUInt16 = native.iqUInt16  # two unsigned 16-bit counts
iqUInt32 = native.iqUInt32  # two unsigned 32-bit counts
iqUInt64 = native.iqUInt64  # two unsigned 64-bit counts

# sized aliases
c32 = complexHalf  # the complex number of 16-bit floats
c64 = complexFloat  # the complex number of 32-bit floats
c128 = complexDouble  # the complex number of 64-bit floats

# numpy names
float16 = half  # numpy's name for the 16-bit float
float32 = float  # numpy's name for the 32-bit float
float64 = double  # numpy's name for the 64-bit float
complex32 = complexHalf  # numpy's name for the complex number of 16-bit floats
complex64 = complexFloat  # numpy's name for the complex number of 32-bit floats
complex128 = complexDouble  # numpy's name for the complex number of 64-bit floats

# standard types - strings
c_s1 = std.c_s1  # a string the way c lays it out
fortran_s1 = std.fortran_s1  # a string the way fortran lays it out


# end of file
