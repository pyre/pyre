# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre
import journal.protocols


# the component declaration
class TextRenderer(pyre.component, family="merlin.renderers.text",
                   implements=journal.protocols.renderer):
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

        # if the message has only one line
        if len(page) == 1:
            # construct the one liner
            yield "{}: {}: {}".format(channel, severity, page[0])
            # all done
            return

        # otherwise, build the first line of the message
        yield "{}: {}:".format(channel, severity)
        # and render the rest
        for line in page: yield line
            
        # all done
        return


# end of file 
