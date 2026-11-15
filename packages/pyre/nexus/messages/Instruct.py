# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my superclass
from .Message import Message


# declaration
class Instruct(Message):
    """
    A journal control applied to the teams, for the staffing agency to apply too, so the members
    it forks from now on start with it in place
    """

    # interface
    def deliver(self, recipient):
        """
        Hand me to {recipient}
        """
        # it applies the control
        return recipient.instruct(order=self)

    # metamethods
    def __init__(self, control, **kwds):
        # chain up
        super().__init__(**kwds)
        # the control, in its wire form
        self.control = control
        # all done
        return


# end of file
