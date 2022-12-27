# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclasses
from .Channel import Channel


# the implementation of the debug channel
class Debug(Channel, active=False, fatal=False):
    """
    Debug channels are used for communicating application progress to developers
    """


    # types
    from .exceptions import DebugError


    # implementation details
    def record(self):
        """
        Make an entry in the journal
        """
        # hunt down my device and record the entry
        self.device.memo(entry=self.entry)
        # all done
        return self


    # constants
    severity = "debug"       # the channel severity
    fatalError = DebugError  # the exception i raise when i'm fatal


# end of file
