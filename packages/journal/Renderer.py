# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the base renderer
class Renderer:
    """
    The base renderer
    """


    # interface
    def render(self, palette, entry):
        """
        Generate the message content
        """
        # each rendered message has three sections
        yield from self.header(palette=palette, entry=entry)
        yield from self.body(palette=palette, entry=entry)
        yield from self.footer(palette=palette, entry=entry)

        # all done
        return


    # implementation details
    def header(self, **kwds):
        """
        Generate the message header
        """
        # nothing to do
        return ()


    def body(self, **kwds):
        """
        Generate the message body
        """
        # nothing to do
        return ()


    def footer(self, **kwds):
        """
        Generate the message footer
        """
        # nothing to do
        return ()


# end of file
