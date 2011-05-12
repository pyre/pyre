# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import pyre


# the implemented interfaces
from .Device import Device


# declaration
class Console(pyre.component, family="journal.devices.console", implements=Device):
    """
    This is a sample documentation string for class Console
    """


    # types
    from .TextRenderer import TextRenderer


    # public state
    renderer = pyre.properties.facility(interface=Device.Renderer, default=TextRenderer)


    # interface
    @pyre.export
    def record(self, page, metadata):
        """
        Record a journal entry
        """
        # get the renderer to produce the text
        for line in self.renderer.render(page, metadata):
            # print it to stdout
            print(line)
        # and return
        return self


# end of file 
