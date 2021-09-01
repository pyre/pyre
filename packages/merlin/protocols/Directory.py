# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# super class
from .Asset import Asset


# class declaration
class Directory(Asset, family="merlin.projects.directories"):
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
        return merlin.projects.directory


# end of file
