# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .File import File


class BlockDevice(File):
    """
    Representation of block devices, a type of unix device driver
    """

    # interface
    def identify(self, explorer, **kwds):
        """
        Tell {explorer} that it is visiting a block device
        """
        return explorer.onBlockDevice(self, **kwds)


    # constant
    marker = 'b'

    
# end of file 
