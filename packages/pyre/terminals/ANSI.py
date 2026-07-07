# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# my base
from .Plain import Plain


# declaration
class ANSI(Plain, family="pyre.terminals.ansi"):
    """
    A terminal that renders color using ANSI control sequences, delegating the sequence
    construction to {pyre::chroma}
    """

    # an ANSI terminal can render color
    chromatic = True

    # interface
    @pyre.export
    def render(self, color):
        """
        Render {color} (a {chroma} color) as a 24-bit truecolor ANSI escape sequence
        """
        # reach the color bindings
        chroma = self._chroma()
        # without them, or without a color to render, there is nothing to emit
        if chroma is None or color is None:
            return ""
        # let chroma serialize the color as a truecolor escape
        return chroma.ansi.rgb(color)

    @pyre.export
    def reset(self):
        """
        The escape sequence that restores the terminal to its default attributes
        """
        # reach the color bindings
        chroma = self._chroma()
        # without them there is nothing to emit
        if chroma is None:
            return ""
        # let chroma produce the reset sequence
        return chroma.ansi.reset()

    @pyre.export
    def hideCursor(self):
        """
        The control sequence that hides the text cursor
        """
        # the DEC private-mode reset that hides the cursor
        return "\x1b[?25l"

    @pyre.export
    def showCursor(self):
        """
        The control sequence that restores the text cursor
        """
        # the DEC private-mode set that shows the cursor
        return "\x1b[?25h"

    @pyre.export
    def rewind(self, lines):
        """
        The control sequence that moves to the top of a {lines}-tall frame and clears downward
        """
        # step up over the previous frame, when there was one
        up = f"\x1b[{lines}A" if lines > 0 else ""
        # then return to the left margin and wipe from the cursor to the end of the screen
        return f"{up}\r\x1b[J"


# end of file
