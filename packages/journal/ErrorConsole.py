# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import sys  # for {stderr}

# superclass
from .Stream import Stream

# the palette definitions and the terminal capability check
from . import palettes
from .ANSI import ANSI


# write messages to {stderr}
class ErrorConsole(Stream):
    """
    Journal device that writes messages to {stderr}
    """

    # metamethods
    def __init__(self, **kwds):
        # colorize only when {stderr} is an interactive, ANSI-compatible terminal
        if sys.stderr.isatty() and ANSI.compatible():
            # use the palette tuned for a light background
            palette = palettes.light
        # otherwise
        else:
            # emit no color
            palette = palettes.null
        # chain up
        super().__init__(name="cerr", stream=sys.stderr, palette=palette, **kwds)
        # all done
        return


# end of file
