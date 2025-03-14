# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import merlin

# super class
from .Asset import Asset


# class declaration
class Folder(Asset, family="merlin.assets.folders"):
    """
    Encapsulation of a container of assets
    """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # publish the default implementation
        return merlin.assets.folder


# end of file
