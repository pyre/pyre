# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import pyre


# declaration
class Renderer(pyre.interface):
    """
    The interface specification that renderers must satisfy
    """


    # interface
    @pyre.provides
    def render(self, text, metadata):
        """
        Convert the diagnostic information into a form that a device can record
        """


# end of file 
