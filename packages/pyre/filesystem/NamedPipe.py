# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .File import File


class NamedPipe(File):
    """
    Representation of named pipes, a unix interprocess communication mechanism
    """


    # constant
    marker = 'p'

    
    # implementation details
    __slots__ = ()

    
# end of file 
