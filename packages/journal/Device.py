# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# packages
import pyre


# declaration
class Device(pyre.protocol, family="journal.devices"):
    """
    The protocol that devices must implement
    """


    # types
    from .Renderer import Renderer


    # public state
    renderer = Renderer()
    renderer.doc = "the formatting strategy"


    # my default implementation
    @classmethod
    def default(cls):
        """
        The default {Device} implementation
        """
        # use {Console}
        from .Console import Console
        return Console


    # interface
    @pyre.provides
    def record(self, page, metadata):
        """
        Create a journal entry from the given information
        """


# end of file 
