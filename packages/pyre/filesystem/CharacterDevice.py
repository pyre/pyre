# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


from .File import File


class CharacterDevice(File):
    """
    Representation of character devices, a type of unix device driver
    """


    # constant
    marker = 'c'

    
    # implementation details
    __slots__ = ()

    
# end of file 
