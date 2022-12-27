# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


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

        # tag using either the app name or the channel severity
        tag  = application or severity
        # generate
        buffer = [
            severityColor, tag, resetColor, ":"
            ]
        # if this is an one liner
        if len(page) == 1:
            # add the page contents to the buffer
            buffer += [
                " ",
                page[0],
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
            yield f"{severityColor}{self.bodyMarker}{bodyColor}{line}{resetColor}"

        # all done
        return


    def footer(self, palette, entry):
        """
        Generate the message body
        """
        # get the page
        page = entry.page
        # if there's nothing to do
        if not page:
            # move on
            return

        # get the notes
        notes = entry.notes
        # grab the severity
        severity = notes["severity"]
        # and the name of the channel
        channel = notes["channel"]

        # get the colors
        resetColor = palette["reset"]
        severityColor = palette[severity]

        # set up the marker
        marker = self.footerMarker
        # grab the chronicler
        from . import chronicler

        # if the chronicler decoration level is sufficiently high
        if chronicler.decor > 1:
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
                    severityColor, self.footerMarker, resetColor,
                    # introduce the locator
                    "at ",
                    # the filename
                    f"{filenameLeader}{ellipsis}{filenameTrailer}:",
                    # the line number
                    f"{line}:" if line else "",
                    # the function name
                    f"{function}" if function else ""
                    ]

                # assemble the line and make it available
                yield ''.join(buffer)

        # if the {chronicler} decoration level is sufficiently high
        if chronicler.decor > 2:
            # render the channel info
            buffer = [
                severityColor, marker, resetColor,
                "because the ",
                severityColor, severity, resetColor,
                " channel '",
                severityColor, channel, resetColor,
                "' is active"
                ]
            # assemble and push
            yield ''.join(buffer)

        # now, for the rest of the metadata
        if chronicler.decor > 1:
            # make a pile of the information we have displayed # already
            done = {
                "severity", "channel", "application",
                "filename", "line", "function", "source",
            }
            # go through the metadata
            for key, value in notes.items():
                # if this is something we've dealt with
                if key in done:
                    # skip it
                    continue
                # otherwise, render it
                buffer = [
                    palette[severity], marker, palette["reset"],
                    palette[severity], key, palette["reset"],
                    ": ",
                    palette[severity], value, palette["reset"],
                    ]
                # assemble and push
                yield ''.join(buffer)

        # all done
        return


    # implementation details
    maxlen = 60
    headerMarker = " >> "
    bodyMarker = " -- "
    footerMarker = " .. "


# end of file
