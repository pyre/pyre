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


    # public state
    header = pyre.properties.str(default=">>")
    header.doc = "the marker to use while rendering the diagnostic metadata"

    body = pyre.properties.str(default="--")
    body.doc = "the marker to use while rendering the diagnostic body"


    # interface
    @pyre.provides
    def render(self, page, metadata):
        """
        Convert the diagnostic information into a form that a device can record
        """
        # build the header
        yield " >> {filename}:{line}:{function}".format(self.header, **metadata)
        yield " >> {name}({severity})".format(self.header, **metadata)
        # and the body
        for line in page:
            yield " {} {} ".format(self.body, line)

        # all done
        return


# end of file 
