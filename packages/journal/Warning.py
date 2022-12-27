# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclasses
from .Channel import Channel


# the implementation of the debug channel
class Warning(Channel, active=True, fatal=False):
    """
    Warning channels are used to communicate application progress to users.

    Typically, they indicate that the application has encountered a condition that is
    potentially problematic, but the application has identified a workaround.
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
    severity = "warning"           # the channel severity
    fatalError = ApplicationError  # the exception i raise when i'm fatal


# end of file
