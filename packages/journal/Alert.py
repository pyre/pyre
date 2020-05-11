# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved


# superclass
from .Renderer import Renderer


# the renderer or user-facing essages
class Alert(Renderer):
    """
    The renderer of user-facing messages
    """


    # implementation details
    def header(self, palette, entry):
        """
        Generate the message header
        """
        # get the page
        page = entry.page

        # if there's nothing to do
        if not page:
            # bail
            return

        # get the notes
        notes = entry.notes

        # get the severity
        severity = notes["severity"]
        # generate
        buffer = [
            palette[severity], notes["application"], palette["reset"],
            "(",
            palette[severity], severity, palette["reset"],
            "): ",
            palette["body"], page[0], palette["reset"]
            ]
        # assemble and push
        yield ''.join(buffer)

        # all done
        return


    def body(self, palette, entry):
        """
        Generate the message body
        """
        # get the page
        page = entry.page

        # if there's nothing to do
        if len(page) < 2:
            # bail
            return

        # otherwise, go through the page contents
        for line in page[1:]:
            # make a buffer
            buffer = [
                palette["body"], line, palette["reset"]
                ]
            # assemble and push
            yield ''.join(buffer)

        # all done
        return


# end of file
