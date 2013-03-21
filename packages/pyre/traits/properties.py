# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
This package provides access to the factories for typed properties
"""


from .Array import Array as array
from .Bool import Bool as bool
from .Dimensional import Dimensional as dimensional
from .Facility import Facility as facility
from .Float import Float as float
from .INet import INet as inet
from .Integer import Integer as int
from .List import List as list
from .Object import Object as object
from .OutputFile import OutputFile as outputfile
from .String import String as str
from .Tuple import Tuple as tuple

# meta-properties
from .Dict import Dict as dict

def catalog(**kwds):
    """
    A {dict} of {list}s
    """
    return dict(schema=list(**kwds))

# end of file 
