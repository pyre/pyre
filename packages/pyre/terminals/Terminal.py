# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre


# declaration
class Terminal(pyre.protocol, family="pyre.terminals"):
    """
    The capabilities of a user terminal
    """

    # configurable state
    # the endpoints the terminal talks to
    istream = pyre.properties.istream()
    istream.default = "stdin"
    istream.doc = "the terminal input stream"

    ostream = pyre.properties.ostream()
    ostream.default = "stdout"
    ostream.doc = "the terminal output stream"

    # whether this terminal type renders color
    chromatic = False

    # requirements
    @pyre.provides
    def interactive(self):
        """
        Whether both endpoints are connected to a live terminal
        """

    @pyre.provides
    def width(self):
        """
        The width of the terminal, in columns
        """

    @pyre.provides
    def height(self):
        """
        The height of the terminal, in rows
        """

    @pyre.provides
    def encoding(self):
        """
        The character encoding of the terminal, or {None} when it cannot be determined
        """

    @pyre.provides
    def render(self, color):
        """
        Render {color} (a {chroma} color) as an escape sequence for this terminal; a terminal
        with no color capability returns the empty string
        """

    @pyre.provides
    def color(self, name):
        """
        The escape sequence for the named color {name}; empty on a terminal with no color, or
        when {name} is not a known color
        """

    @pyre.provides
    def reset(self):
        """
        The escape sequence that restores the terminal to its default attributes; empty on a
        terminal with no color
        """

    @pyre.provides
    def hideCursor(self):
        """
        The control sequence that hides the text cursor; empty on a terminal that cannot
        """

    @pyre.provides
    def showCursor(self):
        """
        The control sequence that restores the text cursor; empty on a terminal that cannot
        """

    @pyre.provides
    def rewind(self, lines):
        """
        The control sequence that moves to the top of a {lines}-tall frame and clears from there
        down; empty on a terminal that cannot
        """

    # framework support
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Sniff out the capabilities of the current terminal and choose the default implementation
        """
        # the standard streams and the shared compatibility check
        import os
        import sys

        from . import compatible

        # try to
        try:
            # check whether output is going to a live terminal
            live = sys.stdout.isatty()
        # some streams have no notion of a terminal
        except AttributeError:
            # so treat them as non-interactive
            live = False

        # the {NO_COLOR} convention lets the user opt out of color regardless of the terminal
        colorless = os.environ.get("NO_COLOR") is not None

        # a live, ANSI-compatible terminal is color capable unless the user opted out
        if live and compatible() and not colorless:
            # so pick the color implementation
            from .ANSI import ANSI

            # and return it
            return ANSI

        # everything else is a plain terminal
        from .Plain import Plain

        # and return it
        return Plain


# end of file
