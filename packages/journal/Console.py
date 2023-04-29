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


# write messages to {stdout}
class Console(Stream):
    """
    Journal device that writes messages to {stdout}
    """


    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(name="cout", stream=sys.stdout, palette=palettes.dark, **kwds)
        # all done
        return


# end of file
