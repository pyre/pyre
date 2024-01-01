# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# superclass
from .File import File


# class declaration
class BlockDevice(File):
    """
    Representation of block devices, a type of unix device driver
    """

    # constant
    marker = "b"

    # interface
    def identify(self, explorer, **kwds):
        """
        Tell {explorer} that it is visiting a block device
        """
        # dispatch
        return explorer.onBlockDevice(info=self, **kwds)


# end of file
