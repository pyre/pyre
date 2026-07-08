# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import os
import sys

# the framework
import pyre


# declaration
class Terminal(pyre.protocol, family="pyre.terminals"):
    """
    The capabilities every terminal provides: device queries, output, and color
    """

    # configurable state
    # the endpoints the terminal talks to
    istream = pyre.properties.istream()
    istream.default = "stdin"
    istream.doc = "the terminal input stream"

    ostream = pyre.properties.ostream()
    ostream.default = "stdout"
    ostream.doc = "the terminal output stream"

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
    def write(self, text):
        """
        Emit {text} to the terminal without a trailing newline
        """

    @pyre.provides
    def flush(self):
        """
        Push any buffered output to the terminal now
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
    def rgb(self, code):
        """
        The escape sequence for a 24-bit color given as a hex string or an integer; empty on a
        terminal with no color, or when {code} is not valid hex
        """

    @pyre.provides
    def reset(self):
        """
        The escape sequence that restores the terminal to its default attributes; empty on a
        terminal with no color
        """

    # capability query
    @classmethod
    def compatible(cls, term=None):
        """
        Report whether the terminal type {term} understands ANSI control sequences; {term}
        defaults to the value of the {TERM} environment variable
        """
        # fall back to the {TERM} environment variable, assuming a dumb terminal when it is unset
        if term is None:
            term = os.environ.get("TERM", "dumb")
        # the terminal is ANSI-capable when its type is one we recognize
        return term.lower() in cls._ansi

    # framework support
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Sniff out the capabilities of the current terminal and choose the default implementation
        """
        # attempt to
        try:
            # check whether output is going to a live terminal
            live = sys.stdout.isatty()
        # some streams have no notion of a terminal
        except AttributeError:
            # so treat them as non-interactive
            live = False

        # a terminal that is not live can neither read keys nor show color
        if not live:
            # so it is a plain terminal
            from .Plain import Plain

            # and that is our answer
            return Plain

        # the {NO_COLOR} convention lets the user opt out of color regardless of the terminal
        colorless = os.environ.get("NO_COLOR") is not None

        # a live, ANSI-compatible terminal is color capable unless the user opted out
        if cls.compatible() and not colorless:
            # so pick the full color implementation
            from .ANSI import ANSI

            # and return it
            return ANSI

        # everything else is a live terminal that cannot, or must not, show color; it still
        # drives a keyboard and a cursor, so it is interactive but colorless
        from .Interactive import Interactive

        # and return it
        return Interactive

    # the set of {TERM} values whose terminals understand ANSI control sequences
    _ansi = {
        "ansi",
        "vt102",
        "vt220",
        "vt320",
        "vt420",
        "xterm",
        "xterm-color",
        "xterm-16color",
        "xterm-256color",
    }


# end of file
