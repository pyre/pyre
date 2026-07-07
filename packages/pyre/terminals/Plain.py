# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import os
import pyre

# my protocol
from .Terminal import Terminal


# declaration
class Plain(pyre.component, family="pyre.terminals.plain", implements=Terminal):
    """
    A terminal with no color capabilities; also the base that carries the shared, {os}-backed
    device queries for every terminal type
    """

    # configurable state
    istream = pyre.properties.istream()
    istream.default = "stdin"
    istream.doc = "the terminal input stream"

    ostream = pyre.properties.ostream()
    ostream.default = "stdout"
    ostream.doc = "the terminal output stream"

    # a plain terminal cannot render color
    chromatic = False

    # interface
    @pyre.export
    def interactive(self):
        """
        Whether both endpoints are connected to a live terminal
        """
        # a redirected or piped end on either side rules out an interactive session
        return self._isatty(self.istream) and self._isatty(self.ostream)

    @pyre.export
    def width(self):
        """
        The width of the terminal, in columns
        """
        # read it off the current terminal size
        return self._size().columns

    @pyre.export
    def height(self):
        """
        The height of the terminal, in rows
        """
        # read it off the current terminal size
        return self._size().lines

    @pyre.export
    def encoding(self):
        """
        The character encoding of the terminal, or {None} when it cannot be determined
        """
        # try to
        try:
            # ask the operating system about the output endpoint
            return os.device_encoding(self.ostream.fileno())
        # when there is no descriptor or no terminal
        except (AttributeError, OSError):
            # the encoding is unknown
            return None

    @pyre.export
    def render(self, color):
        """
        Render {color} as an escape sequence; a plain terminal emits none
        """
        # a plain terminal has no color
        return ""

    @pyre.export
    def color(self, name):
        """
        The escape sequence for the named color {name}; empty on a colorless terminal, or when
        {name} is not a known color
        """
        # a colorless terminal renders nothing
        if not self.chromatic:
            return ""
        # otherwise resolve the name to a color and render it
        return self.render(self._lookup(name))

    @pyre.export
    def reset(self):
        """
        The escape sequence that restores the terminal to its default attributes
        """
        # a plain terminal has nothing to reset
        return ""

    # implementation details
    def _lookup(self, name):
        """
        Resolve a color {name} to a {chroma} color, or {None} when unavailable or unknown
        """
        # reach the color bindings
        chroma = self._chroma()
        # without them there is no color
        if chroma is None:
            return None
        # look the name up in chroma's palette
        return chroma.rgb.palette.find(name)

    def _chroma(self):
        """
        Access the {chroma} color bindings, or {None} when they are unavailable (e.g. bootstrap)
        """
        # the framework carries the bindings
        import pyre

        # they live on {libpyre}, which is absent when the extension was not built
        return None if pyre.libpyre is None else pyre.libpyre.chroma

    def _size(self):
        """
        Query the terminal window size, falling back to zeros when there is no terminal
        """
        # try to
        try:
            # ask the operating system, using the output endpoint
            return os.get_terminal_size(self.ostream.fileno())
        # a missing descriptor or absent terminal
        except (AttributeError, ValueError, OSError):
            # leaves the size unknown
            return os.terminal_size((0, 0))

    def _isatty(self, stream):
        """
        Whether {stream} is connected to a terminal
        """
        # try to
        try:
            # ask the operating system about the stream's descriptor
            return os.isatty(stream.fileno())
        # a stream without a descriptor
        except (AttributeError, ValueError, OSError):
            # is not a terminal
            return False


# end of file
