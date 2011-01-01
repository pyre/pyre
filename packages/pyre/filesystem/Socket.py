# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .File import File


class Socket(File):
    """
    Representation of sockets, a type of interprocess communication mechanism
    """


    # interface
    def identify(self, explorer, **kwds):
        """
        Tell {explorer} that it is visiting a socket
        """
        return explorer.onSocket(self, **kwds)


    # constant
    marker = 's'

    
# end of file 
