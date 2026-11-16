# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my superclass
from .Message import Message


# declaration
class Recruited(Message):
    """
    The staffing agency's answer to a recruitment request: the pids of the members it forked, in
    the order the request listed them
    """

    # interface
    def deliver(self, recipient):
        """
        Hand me to {recipient}
        """
        # it is waiting for the answer
        return recipient.recruited(answer=self)

    # metamethods
    def __init__(self, pids, **kwds):
        # chain up
        super().__init__(**kwds)
        # the pids of the new members
        self.pids = list(pids)
        # all done
        return


# end of file
