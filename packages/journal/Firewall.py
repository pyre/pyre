# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclasses
from .Channel import Channel


# the implementation of the Firewall channel
class Firewall(Channel, active=True, fatal=True):
    """
    Firewalls are used to communicate that a bug was detected.

    Firewalls are typically used to contain code that enforces invariants and checks the
    internal consistency of the code. When these checks fail, the firewall prints a diagnostic
    message to the screen and raises an exception.

    A firewall fires either because a defect has been identified or because the defect
    detection logic in the firewall is faulty. In either case, THE SOURCE CODE REQUIRES
    MODIFICATION.

    Expensive consistency checks can be avoided by checking whether the associated firewall is
    active before conducting them.
    """


    # types
    from .exceptions import FirewallError


    # implementation details
    def record(self):
        """
        Commit my payload to the journal
        """
        # hunt down my device and record the entry
        self.device.memo(entry=self.entry)
        # return the exception that would have been raised if i were fatal
        return self.complaint()


    # constants
    severity = "firewall"       # the channel severity
    fatalError = FirewallError  # the exception i raise when i'm fatal


# end of file
