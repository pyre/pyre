# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


from .File import File


class Directory(File):
    """
    Representation of local filesystem folders
    """


    # constants
    marker = 'd'
    isDirectory = True

    
    # implementation details
    __slots__ = ()

    
# end of file 
