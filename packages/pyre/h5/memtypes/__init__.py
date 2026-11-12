# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


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

# radar samples: a pair of counts of each integer type
from .IQInt8 import iqInt8
from .IQInt16 import iqInt16
from .IQInt32 import iqInt32
from .IQInt64 import iqInt64
from .IQUInt8 import iqUInt8
from .IQUInt16 import iqUInt16
from .IQUInt32 import iqUInt32
from .IQUInt64 import iqUInt64

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
