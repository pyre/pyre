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


    # interface
    def identify(self, explorer, **kwds):
        """
        Tell {explorer} that it is visiting a named pipe
        """
        return explorer.onNamedPipe(self, **kwds)


    # constant
    marker = 'p'

    
# end of file 
