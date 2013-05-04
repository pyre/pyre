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
from .Object import Object as object
from .OutputFile import OutputFile as outputfile
from .String import String as str


# meta-properties: trait descriptors for homogeneous containers; these require other trait
# descriptors to specify the type of the contents
from .Dict import Dict as dict
from .List import List as list
from .Set import Set as set
from .Tuple import Tuple as tuple


def pathlist(**kwds):
    """
    A {list} of {str}ings that represent uris
    """
    return list(schema=str(**kwds))


def catalog(**kwds):
    """
    A {dict} of {list}s
    """
    return dict(schema=list(**kwds))


# end of file 
