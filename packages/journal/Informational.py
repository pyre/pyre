# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclasses
from .Channel import Channel


# the implementation of the debug channel
class Informational(Channel, active=True, fatal=False):
    """
    Informational channels are used for communicating application progress to users
    """


    # types
    from .exceptions import ApplicationError


    # implementation details
    def record(self):
        """
        Commit my payload to the journal
        """
        # hunt down my device and record the entry
        self.device.alert(entry=self.entry)
        # all done
        return self


    # constants
    severity = "info"              # the channel severity
    fatalError = ApplicationError  # the exception i raise when i'm fatal


# end of file
