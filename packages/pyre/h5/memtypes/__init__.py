# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved

# the base class
from .MemoryType import MemoryType as type

# c types
from .Char import char
from .SignedChar import signedChar
from .UnsignedChar import unsignedChar
from .Short import short
from .UnsignedShort import unsignedShort
from .Int import int
from .UnsignedInt import unsignedInt
from .Long import long
from .UnsignedLong import unsignedLong

# specification with a guaranteed size
# signed
from .Int8 import int8
from .Int16 import int16
from .Int32 import int32
from .Int64 import int64

# unsigned
from .UInt8 import uint8
from .UInt16 import uint16
from .UInt32 import uint32
from .UInt64 import uint64


# floating point
from .Float import float
from .Double import double

# complex numbers
# regular
from .ComplexFloat import complexFloat
from .ComplexDouble import complexDouble

# built out of integer types
from .ComplexInt8 import complexInt8
from .ComplexInt16 import complexInt16
from .ComplexInt32 import complexInt32
from .ComplexInt64 import complexInt64

# aliases
r32 = float
r64 = double
c64 = complexFloat
c128 = complexDouble

float32 = float
float64 = double
complex64 = complexFloat
complex128 = complexDouble

# end of file
