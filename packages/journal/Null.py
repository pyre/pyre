# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the implementation of the null channel
class Null:
    """
    Null channels implement the channel interface correctly but are no-ops
    """

    # my state
    @property
    def active(self):
        """
        Null channels are never active
        """
        # always off
        return False

    @active.setter
    def active(self, active):
        """
        Ignore attempts to turn me on
        """
        # ignore
        return

    @property
    def fatal(self):
        """
        Null channels are never fatal
        """
        # never
        return False

    @fatal.setter
    def fatal(self, fatal):
        """
        Ignore attempts to make me fatal
        """
        # ignore
        return

    # my device
    @property
    def device(self):
        """
        Null channels have no device
        """
        # and always null
        return None

    @device.setter
    def device(self, device):
        """
        Ignore attempts to give me a {device}
        """
        # ignore
        return

    # interface
    def activate(self):
        """
        Ignore requests to turn me on
        """
        # ignore
        return self

    def deactivate(self):
        """
        Ignore requests to turn me off, since I am never on
        """
        # ignore
        return self

    def line(self, *args, **kwds):
        """
        Discard the line
        """
        # do nothing
        return

    def log(self, *args, **kwds):
        """
        Discard the entry
        """
        # do nothing
        return self

    # access to severity wide configuration
    @classmethod
    def activateChannels(cls, names):
        """
        Ignore requests to activate the channels in {names}
        """
        # ignore
        return

    @classmethod
    def getDefaultDevice(cls):
        """
        Null channels have no default device
        """
        # easy enough
        return None

    @classmethod
    def setDefaultDevice(cls, device):
        """
        Ignore attempts to set the default {device}
        """
        # ignore
        return None

    # metamethods
    def __init__(self, **kwds):
        """
        Absorb my construction arguments
        """
        # absorb all
        return

    def __bool__(self):
        """
        Simplify state testing
        """
        return self.active

    # implementation details
    def commit(self):
        """
        Commit my payload to the journal
        """
        # do nothing
        return self

    # constant
    severity = "null"  # the channel severity


# end of file
