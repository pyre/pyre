# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import contextlib
import os
import select
import termios
import tty

import pyre

# my base and the extra capability it fulfils
from .Plain import Plain
from .Console import Console as console

# the key decoder
from . import keys


# declaration
class Interactive(Plain, family="pyre.terminals.interactive", implements=console):
    """
    A live terminal: still colorless, but connected to a real keyboard and cursor, so it can read
    keypresses one at a time and drive an interactive redraw loop
    """

    # interface
    @pyre.export
    @contextlib.contextmanager
    def rawmode(self):
        """
        Put the terminal in cbreak mode for the duration of the {with} block so keys arrive one
        at a time, restoring the cooked settings on the way out
        """
        # resolve the input descriptor now that we actually need raw mode
        self._fd = self.istream.fileno()
        # remember the cooked settings so we can restore them however we leave
        self._saved = termios.tcgetattr(self._fd)
        # try to
        try:
            # switch to cbreak so keys arrive immediately while ctrl-c still raises
            # {KeyboardInterrupt} rather than arriving as a byte
            tty.setcbreak(self._fd)
            # hand control to the {with} body
            yield self
        # on the way out, no matter what
        finally:
            # restore the terminal the user handed us
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._saved)
            # and reset the raw-mode bookkeeping
            self._fd = None
            self._saved = None

    @pyre.export
    def readkey(self):
        """
        Read and decode a single logical keypress
        """
        # let the decoder pull bytes through our blocking and non-blocking readers
        return keys.decode(self._nextbyte, self._pending)

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

    # implementation details
    def _nextbyte(self):
        """
        Block for the next input byte, or {None} when the input is exhausted
        """
        # a blocking read of one byte
        data = os.read(self._fd, 1)
        # its value, or {None} when the input is exhausted
        return data[0] if data else None

    def _pending(self):
        """
        Return an already-waiting input byte without blocking, or {None} when none is waiting
        """
        # ask whether a byte is already waiting, without blocking
        ready, _, _ = select.select([self._fd], [], [], 0.005)
        # nothing waiting means an escape sequence has ended
        if not ready:
            # so report the absence
            return None
        # otherwise take the byte that is ready
        data = os.read(self._fd, 1)
        # its value, or {None} at the end of input
        return data[0] if data else None

    # raw-mode bookkeeping, populated only while a {rawmode} block is active
    _fd = None
    _saved = None


# end of file
