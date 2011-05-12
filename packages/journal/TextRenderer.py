# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import pyre


# the implemented interfaces
from .Renderer import Renderer


# declaration
class TextRenderer(pyre.component, family="journal.renderers.text", implements=Renderer):
    """
    This is a sample documentation string for class Console
    """


    # interface
    @pyre.provides
    def render(self, page, metadata):
        """
        Convert the diagnostic information into a form that a device can record
        """
        # build the header
        yield " >> {filename}:{line}:{function}".format(**metadata)
        yield " >> {name}({severity})".format(**metadata)
        # and the body
        for line in page:
            yield " -- " + line

        # all done
        return


# end of file 
