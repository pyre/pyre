# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Renderer import Renderer


# the renderer or developer-facing messages
class Bland(Renderer):
    """
    The renderer of user-facing messages
    """


    # implementation details
    def body(self, palette, entry):
        """
        Generate the message body
        """
        # get the page
        page = entry.page
        # indent
        indent = " " * 2
        # go through the message content
        for line in page:
            # and print each line
            yield f"{indent}{line}"
        # all done
        return


# end of file
