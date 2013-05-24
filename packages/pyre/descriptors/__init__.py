# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# the descriptor base class
from .Descriptor import descriptor

# decorators for value processors
from .Converter import Converter as converter
from .Normalizer import Normalizer as normalizer
from .Validator import Validator as validator


# simple typed descriptors
from .Bool import Bool as bool
from .Decimal import Decimal as decimal
from .Dimensional import Dimensional as dimensional
from .Float import Float as float
from .INet import INet as inet
from .Integer import Integer as int
from .Object import Object as object
from .String import String as str
from .URI import URI as uri


# end of file 
