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
        # get the metadata
        channel = notes["channel"]
        severity = notes["severity"]
        application = notes["application"]

        # get the colors
        resetColor = palette["reset"]
        severityColor = palette[severity]

        # generate
        buffer = [
            severityColor, application, resetColor,
            " ",
            severityColor, severity, resetColor,
            ": ",
            severityColor, channel, resetColor,
            ":",
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
        if not page:
            # bail
            return

        # get the notes
        notes = entry.notes
        # get the metadata
        severity = notes["severity"]

        # get the colors
        resetColor = palette["reset"]
        bodyColor = palette["body"]
        severityColor = palette[severity]

        # otherwise, go through the page contents
        for line in page:
            # assemble and push
            yield f"{severityColor}{self.marker}{bodyColor}{line}{resetColor}"

        # get the name of the file
        filename = notes["filename"]
        # get the line number
        line = str(notes["line"])
        # get the function name
        function = notes["function"]

        # consider it an indication that we have location information
        if filename:
            # lookup the longest filename we are going to print
            maxlen = self.maxlen
            # if the filename is too long
            if len(filename) > maxlen:
                # compute the leading part
                filenameLeader = filename[:maxlen//4-3]
                # the ellipsis
                ellipsis = "..."
                # and the trailing part of the filename
                filenameTrailer = filename[-3*maxlen//4:]
            # otherwise
            else:
                # the leading part is the whole thing
                filenameLeader = filename
                # no ellipsis
                ellipsis = ""
                # no trailing part
                filenameTrailer = ""

            # make a buffer
            buffer = [
                # a marker
                severityColor, self.marker, bodyColor,
                # the filename
                f"{filenameLeader}{ellipsis}{filenameTrailer}:",
                # the line number
                f"{line}:" if line else "",
                # the function name
                f"{function}" if function else ""
                ]

            # assemble the line and make it available
            yield ''.join(buffer)

        # all done
        return


    # implementation details
    maxlen = 60
    marker = " >> "


# end of file
