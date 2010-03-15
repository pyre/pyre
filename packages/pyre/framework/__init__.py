# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
This packages contains the various top level framework managers
"""


def executive(**kwds):
    """
    Factory for the framework executive.

    The pyre executive is a singleton that builds and maintains the collection of top-level
    framework objects that provide the runtime framework services
    """
    from .Pyre import Pyre
    return Pyre(**kwds)


# end of file 
