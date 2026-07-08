# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import sys  # for {stdout}

# superclass
from .Stream import Stream

# the palette definitions and the terminal capability check
from . import palettes
from .ANSI import ANSI


# write messages to {stdout}
class Console(Stream):
    """
    Journal device that writes messages to {stdout}
    """

    # metamethods
    def __init__(self, **kwds):
        # colorize only when {stdout} is an interactive, ANSI-compatible terminal
        if sys.stdout.isatty() and ANSI.compatible():
            # use the palette tuned for a dark background
            palette = palettes.dark
        # otherwise
        else:
            # emit no color
            palette = palettes.null
        # chain up
        super().__init__(name="cout", stream=sys.stdout, palette=palette, **kwds)
        # all done
        return


# end of file
