# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# superclass
from .File import File

# class declaration
class Socket(File):
    """
    Representation of sockets, a type of interprocess communication mechanism
    """

    # constant
    marker = 's'

    # implementation details
    __slots__ = ()


# end of file
