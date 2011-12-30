# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


from .File import File


class Socket(File):
    """
    Representation of sockets, a type of interprocess communication mechanism
    """


    # constant
    marker = 's'


    # implementation details
    __slots__ = ()

    
# end of file 
