# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import sys  # for {stdout}

# superclass
from .Stream import Stream

# the palette definitions
from . import palettes


# write messages to a log file
class File(Stream):
    """
    Journal device that writes messages to the file at {path}
    """

    # the default mode for opening the stream
    mode = "w"

    # metamethods
    def __init__(self, path, mode=mode, **kwds):
        """
        Open the file at {path} with {mode}, and write entries to it
        """
        # chain up
        super().__init__(name="file", stream=open(path, mode=mode), **kwds)
        # save the path
        self.path = path
        # all done
        return


# end of file
