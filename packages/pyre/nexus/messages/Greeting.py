# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my superclass
from .Message import Message


# declaration
class Greeting(Message):
    """
    The first thing the staffing agency says: a description of what it runs, so its liaison can
    prove it runs what the team's process runs
    """

    # interface
    def deliver(self, recipient):
        """
        Hand me to {recipient}
        """
        # it checks what i describe
        return recipient.greeted(greeting=self)

    # metamethods
    def __init__(self, fingerprint, **kwds):
        # chain up
        super().__init__(**kwds)
        # what the agency runs
        self.fingerprint = fingerprint
        # all done
        return


# end of file
