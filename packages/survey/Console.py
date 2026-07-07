# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import select
import termios
import tty

# the framework, for the terminal the user is connected to
import pyre

# the local key decoder
from . import keys


class Console:
    """
    A raw-mode view of the terminal: reads keypresses one at a time and draws prompt frames
    """

    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the terminal the user is connected to
        self._terminal = pyre.executive.terminal
        # its input and output streams
        self._istream = self._terminal.istream
        self._ostream = self._terminal.ostream
        # resolve the input descriptor lazily, only when we enter raw mode, so a {Console}
        # over streams without one stays usable on the non-interactive paths
        self._fd = None
        # nowhere to stash the cooked-mode settings until we actually take raw mode
        self._saved = None

    def interactive(self) -> bool:
        """
        Report whether both ends are a real terminal, so a live UI is possible
        """
        # defer to the terminal's own assessment
        return self._terminal.interactive()

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
        # nothing to hand back
        return

    def flush(self) -> None:
        """
        Push any buffered output to the terminal now
        """
        # drain the output buffer
        self._ostream.flush()
        # nothing to hand back
        return

    def hideCursor(self) -> None:
        """
        Hide the text cursor while a frame is being redrawn
        """
        # emit the terminal's hide-cursor sequence
        self.write(self._terminal.hideCursor())
        # and make sure it takes effect immediately
        self.flush()
        # nothing to hand back
        return

    def showCursor(self) -> None:
        """
        Restore the text cursor once interaction is done
        """
        # emit the terminal's show-cursor sequence
        self.write(self._terminal.showCursor())
        # and make sure it takes effect immediately
        self.flush()
        # nothing to hand back
        return

    def rewind(self, *, lines: int) -> None:
        """
        Move the cursor to the top of a frame {lines} tall and clear from there down
        """
        # emit the terminal's rewind sequence for a frame this tall
        self.write(self._terminal.rewind(lines))
        # nothing to hand back
        return

    def __enter__(self) -> "Console":
        # resolve the input descriptor now that we actually need raw mode
        self._fd = self._istream.fileno()
        # remember the cooked settings so we can restore them on the way out
        self._saved = termios.tcgetattr(self._fd)
        # switch to cbreak so keys arrive immediately while ctrl-c still raises
        # {KeyboardInterrupt} rather than arriving as a byte
        tty.setcbreak(self._fd)
        # hand ourselves to the {with} body
        return self

    def __exit__(self, *exc) -> bool:
        # always restore the terminal the user handed us, even on an exception
        termios.tcsetattr(self._fd, termios.TCSADRAIN, self._saved)
        # do not suppress whatever exception may be propagating
        return False

    def _nextbyte(self):
        # a blocking read of one byte
        data = os.read(self._fd, 1)
        # its value, or {None} when the input is exhausted
        return data[0] if data else None

    def _pending(self):
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


# end of file
