# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclasses
from .Channel import Channel


# the implementation of the help channel
class Help(Channel, active=True, fatal=False):
    """
    Help channels are used for communicating usage instructions to end users
    """


    # types
    from .exceptions import ApplicationError


    # implementation details
    def record(self):
        """
        Make an entry in the journal
        """
        # hunt down my device and record the entry
        self.device.help(entry=self.entry)
        # all done
        return self


    # constants
    severity = "help"              # the channel severity
    fatalError = ApplicationError  # the exception i raise when i'm fatal


# end of file
