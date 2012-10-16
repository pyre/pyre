# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# superclass
from .File import File


# class declaration
class BlockDevice(File):
    """
    Representation of block devices, a type of unix device driver
    """

    # constant
    marker = 'b'
    
    # implementation details
    __slots__ = ()

    
# end of file 
