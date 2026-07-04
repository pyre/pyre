# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import select
import sys
import termios
import tty

# the local key decoder
from . import keys


class Console:
    """
    A raw-mode view of the terminal: reads keypresses one at a time and draws prompt frames
    """

    def __init__(self, *, istream=None, ostream=None, **kwds):
        super().__init__(**kwds)
        # the streams to talk to, defaulting to the process standard streams
        self._istream = istream if istream is not None else sys.stdin
        self._ostream = ostream if ostream is not None else sys.stdout
        # the input file descriptor, which is what {termios} operates on
        self._fd = self._istream.fileno()
        # a place to stash the cooked-mode settings while we are in raw mode
        self._saved = None

    def interactive(self) -> bool:
        """
        Report whether both ends are a real terminal, so a live UI is possible
        """
        # a redirected or piped stream cannot drive an interactive prompt
        return self._istream.isatty() and self._ostream.isatty()

    def readkey(self) -> "keys.Key":
        """
        Read and decode a single logical keypress
        """
        # let the decoder pull bytes through our blocking and non-blocking readers
        return keys.decode(self._nextbyte, self._pending)

    def write(self, text: str) -> None:
        """
        Emit {text} to the terminal without a trailing newline
        """
        # write straight through; callers decide where lines break
        self._ostream.write(text)
        return

    def flush(self) -> None:
        """
        Push any buffered output to the terminal now
        """
        self._ostream.flush()
        return

    def hideCursor(self) -> None:
        """
        Hide the text cursor while a frame is being redrawn
        """
        self.write("\x1b[?25l")
        self.flush()
        return

    def showCursor(self) -> None:
        """
        Restore the text cursor once interaction is done
        """
        self.write("\x1b[?25h")
        self.flush()
        return

    def rewind(self, *, lines: int) -> None:
        """
        Move the cursor to the top of a frame {lines} tall and clear from there down
        """
        # step up over the previous frame, when there was one
        if lines > 0:
            self.write(f"\x1b[{lines}A")
        # then wipe everything from the cursor to the end of the screen
        self.write("\r\x1b[J")
        return

    def __enter__(self) -> "Console":
        # remember the cooked settings, then switch to cbreak so keys arrive immediately
        # while ctrl-c still raises {KeyboardInterrupt} rather than arriving as a byte
        self._saved = termios.tcgetattr(self._fd)
        tty.setcbreak(self._fd)
        return self

    def __exit__(self, *exc) -> bool:
        # always restore the terminal the user handed us, even on an exception
        termios.tcsetattr(self._fd, termios.TCSADRAIN, self._saved)
        return False

    def _nextbyte(self):
        # a blocking read of one byte, or {None} when the input is exhausted
        data = os.read(self._fd, 1)
        return data[0] if data else None

    def _pending(self):
        # a byte only if one is already waiting, so escape sequences do not stall the reader
        ready, _, _ = select.select([self._fd], [], [], 0.005)
        if not ready:
            return None
        data = os.read(self._fd, 1)
        return data[0] if data else None


# end of file
