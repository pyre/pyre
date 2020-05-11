# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved


# superclass
from .Renderer import Renderer


# the renderer or developer-facing essages
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

        # setup the marker
        marker = self.marker
        # otherwise, grab the severity
        severity = notes["severity"]

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

        # render the channel name and severity
        buffer = [
            palette[severity], marker, palette["reset"],
            palette[severity], notes["channel"], palette["reset"],
            "(", palette[severity], severity, palette["reset"], ")"
            ]
        # assemble and push
        yield ''.join(buffer)

        # now, for the rest of the metadata; make a pile of the information we have displayed
        # already
        done = { "severity", "channel", "filename", "line", "function", "source" }
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
        marker = self.continuation
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


    # implementation details
    maxlen = 60
    marker = " >> "
    continuation = " -- "


# end of file
