# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .File import File


class NamedPipe(File):
    """
    Representation of named pipes, a unix interprocess communication mechanism
    """


    def identify(self, explorer, **kwds):
        """
        Tell {explorer} that it is visiting a named pipe
        """
        return explorer.onNamedPipe(self, **kwds)


# end of file 
