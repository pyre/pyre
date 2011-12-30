# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre
import journal.interfaces


# the component declaration
class TextRenderer(pyre.component, family="merlin.renderers.text",
                   implements=journal.interfaces.renderer):
    """
    Custom replacement for the {journal} renderer
    """


    # interface
    @pyre.export
    def render(self, page, metadata):
        """
        Convert the diagnostic information into a form that a device can record
        """
        # extract the information from the metadata
        channel = metadata['channel']
        severity = metadata['severity']

        # make an iterator over the message contents
        lines = iter(page)
        # build the first line of the message
        yield "{}: {}: {}".format(channel, severity, next(lines))
        # and render the rest
        for line in lines: yield line

        # all done
        return


# end of file 
