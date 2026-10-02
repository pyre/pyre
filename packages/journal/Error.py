# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from .Channel import Channel


# the implementation of the debug channel
class Error(Channel, active=True, fatal=True):
    """
    Error channels are used to communicate application progress to users

    Typically, they indicate that the application has encountered a condition that is
    problematic, and the application is unable to identify a viable workaround.
    """

    # types
    from .exceptions import ApplicationError

    # implementation details
    def outcome(self):
        """
        What recording an entry leads to: the exception that states the condition, so the
        caller can raise it whether i am fatal or not
        """
        # build the exception and hand it off
        return self.complaint()

    def record(self):
        """
        Commit my payload to the journal
        """
        # hunt down my device and record the entry
        self.device.alert(entry=self.entry)
        # all done
        return self

    # constants
    severity = "error"  # the channel severity
    headline = "application error"  # the summary of the condition when i'm fatal
    fatalError = ApplicationError  # the exception i raise when i'm fatal


# end of file
