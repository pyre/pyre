# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# c types
# char
from .Char import Char as char
from .SignedChar import SignedChar as signedChar
from .UnsignedChar import UnsignedChar as unsignedChar
from .Short import Short as short
from .UnsignedShort import UnsignedShort as unsignedShort
from .Int import Int as int
from .UnsignedInt import UnsignedInt as unsignedInt
from .Long import Long as long
from .UnsignedLong import UnsignedLong as unsignedLong

from .Float import Float as float
from .Double import Double as double
from .ComplexFloat import ComplexFloat as complexFloat
from .ComplexDouble import ComplexDouble as complexDouble

# specification with a guaranteed size
# signed
from .Int8 import Int8 as int8
from .Int16 import Int16 as int16
from .Int32 import Int32 as int32
from .Int64 import Int64 as int64

# unsigned
from .UInt8 import UInt8 as uint8
from .UInt16 import UInt16 as uint16
from .UInt32 import UInt32 as uint32
from .UInt64 import UInt64 as uint64

# floats
from .Float import Float as real32
from .Double import Double as real64
from .ComplexFloat import ComplexFloat as complex64
from .ComplexDouble import ComplexDouble as complex128


# end of file
