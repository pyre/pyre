# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import sys # for {stdout}
# superclass
from .Stream import Stream
# the palette definitions
from . import palettes


# write messages to {stderr}
class ErrorConsole(Stream):
    """
    Journal device that writes messages to {stderr}
    """


    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(name="cerr", stream=sys.stderr, palette=palettes.light, **kwds)
        # all done
        return


# end of file
