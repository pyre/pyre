# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import pyre


# declaration
class Device(pyre.interface, family="journal.devices"):
    """
    The interface that devices must implement
    """


    # types
    from .Renderer import Renderer


    # public state
    renderer = pyre.properties.facility(interface=Renderer)


    # interface
    @pyre.provides
    def record(self, page, metadata):
        """
        Create a journal entry from the given information
        """


# end of file 
