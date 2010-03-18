# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .File import File


class CharacterDevice(File):
    """
    Representation of character devices, a type of unix device driver
    """


    def identify(self, explorer, **kwds):
        """
        Tell {explorer} that it is visiting a character device
        """
        return explorer.onCharacterDevice(self, **kwds)


# end of file 
