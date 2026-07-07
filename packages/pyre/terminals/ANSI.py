# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# my base
from .Interactive import Interactive


# declaration
class ANSI(Interactive, family="pyre.terminals.ansi"):
    """
    A live terminal that also renders color using ANSI control sequences, delegating the sequence
    construction to {pyre::chroma}
    """

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


# end of file
