# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre


# declaration
class Console(pyre.protocol, family="pyre.terminals.console"):
    """
    The extra capabilities of a live terminal: raw keypress input and cursor control, the pieces
    an interactive redraw loop needs but a redirected stream cannot offer
    """

    # requirements
    @pyre.provides
    def rawmode(self):
        """
        A context manager that puts the terminal in raw mode for its duration so keypresses
        arrive one at a time
        """

    @pyre.provides
    def readkey(self):
        """
        Read and decode a single logical keypress, returning a {keys.Key}
        """

    @pyre.provides
    def hideCursor(self):
        """
        The control sequence that hides the text cursor
        """

    @pyre.provides
    def showCursor(self):
        """
        The control sequence that restores the text cursor
        """

    @pyre.provides
    def rewind(self, lines):
        """
        The control sequence that moves to the top of a {lines}-tall frame and clears from there
        down
        """


# end of file
