# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Asset import Asset
# schema
from .Language import Language as language


# class declaration
class Source(Asset, family="merlin.projects.sources"):
    """
    Encapsulation of a file with source code
    """


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # grab the library foundry and return it
        return merlin.projects.source


# end of file
