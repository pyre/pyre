# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# super class
from .Asset import Asset


# class declaration
class Auxiliary(Asset, family="merlin.projects.auxiliaries"):
    """
    Encapsulation of an auxiliary file
    """


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # publish the default implementation
        return merlin.projects.auxiliary


# end of file
