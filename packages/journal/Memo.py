# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Renderer import Renderer


# the renderer or developer-facing messages
class Memo(Renderer):
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
        # if there is nothing to render
        if not page:
            # bail
            return

        # get the notes
        notes = entry.notes
        # grab the severity
        severity = notes["severity"]

        # setup the marker
        marker = self.headerMarker

        # get the name of the file
        filename = notes["filename"]
        # consider it an indication that we have location information
        if filename:
            # initialize a buffer
            buffer = [ palette[severity] ]
            # pull the longest filename we are going to print
            maxlen = self.maxlen
            # if the filename is too long
            if len(filename) > maxlen:
                # place a leading part in the buffer
                buffer.append(filename[:maxlen//4-3])
                # add an ellipsis
                buffer.append("...")
                # and the trailing part of the filename
                buffer.append(filename[-3*maxlen//4:])
            # otherwise
            else:
                # add the filename to pile
                buffer.append(filename)
            # in any case, reset the color
            buffer.append(palette["reset"])
            # and add a spacer
            buffer.append(":")

            # get the line number
            line = str(notes["line"])
            # if it's available
            if line:
                # turn color back on
                buffer.append(palette[severity])
                # add the number to the pile
                buffer.append(line)
                # reset the color
                buffer.append(palette["reset"])
                # and add a spacer
                buffer.append(":")

            # repeat with the function name
            function = notes["function"]
            # if it's available
            if function:
                # turn color back on
                buffer.append(palette[severity])
                # add the number to the pile
                buffer.append(function)
                # reset the color
                buffer.append(palette["reset"])
                # and add a spacer
                buffer.append(":")

            # assemble the line and make it available
            yield ''.join(buffer)
        # if we don't have location information
        else:
            # just print the channel severity
            buffer = [
                palette[severity],
                severity,
                palette["reset"],
                ":",
            ]
            # assemble the line and make it available
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
            # move on
            return

        # get the notes
        notes = entry.notes

        # get the marker
        marker = self.bodyMarker
        # and the severity
        severity = notes["severity"]

        # go through the message content
        for line in page:
            # render
            buffer = [
                palette[severity], marker, palette["reset"],
                palette["body"], line, palette["reset"]
                ]
            # assemble and push
            yield ''.join(buffer)

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

        # set up the marker
        marker = self.footerMarker
        # grab the chronicler
        from . import chronicler

        # if the {chronicler} decoration level is sufficiently high
        if chronicler.decor > 2:
            # look up the application name
            app = notes.get("application")
            # if we know it
            if app:
                # render it
                buffer = [
                    palette[severity], marker, palette["reset"],
                    "from application ",
                    palette[severity], app, palette["reset"],
                ]
                # assemble and push
                yield ''.join(buffer)

            # render the channel info
            buffer = [
                palette[severity], marker, palette["reset"],
                "because the ",
                palette[severity], severity, palette["reset"],
                " channel '",
                palette[severity], channel, palette["reset"],
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
