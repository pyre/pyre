# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .File import File


class CharacterDevice(File):
    """
    Representation of character devices, a type of unix device driver
    """


    # interface
    def identify(self, explorer, **kwds):
        """
        Tell {explorer} that it is visiting a character device
        """
        return explorer.onCharacterDevice(self, **kwds)


    # constant
    marker = 'c'

    
# end of file 
