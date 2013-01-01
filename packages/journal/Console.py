# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# packages
import pyre


# the implemented interfaces
from .Device import Device


# declaration
class Console(pyre.component, family="journal.devices.console", implements=Device):
    """
    A device that sends journal messages to the standard output
    """


    # public state
    renderer = Device.Renderer()
    renderer.doc = "the formatting strategy for journal entries"


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
