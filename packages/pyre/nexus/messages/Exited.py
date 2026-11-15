# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my superclass
from .Message import Message


# declaration
class Exited(Message):
    """
    The staffing agency's report that one of the members it forked is gone: only the agency can
    collect its exit status, since the member is its child
    """

    # interface
    def deliver(self, recipient):
        """
        Hand me to {recipient}
        """
        # it tells the recruiters that are waiting for the member
        return recipient.exited(report=self)

    # metamethods
    def __init__(self, pid, status, **kwds):
        # chain up
        super().__init__(**kwds)
        # the member that is gone
        self.pid = pid
        # and its exit status
        self.status = status
        # all done
        return


# end of file
