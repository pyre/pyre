# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the implementation of the null channel
class Null:
    """
    Null channels implement the channel interface correctly but are no-ops
    """


    # my state
    @property
    def state(self):
        # if always off
        return False


    @state.setter
    def state(self, state):
        # ignore
        return


    # my device
    @property
    def device(self):
        # and always null
        return None


    @device.setter
    def device(self, device):
        # ignore
        return


    # interface
    def activate(self):
        # ignore
        return self


    def deactivate(self):
        # ignore
        return self


    def line(self, *args, **kwds):
        # do nothing
        return


    def log(self, *args, **kwds):
        # do nothing
        return self


    # access to severity wide configuration
    @classmethod
    def getDefaultDevice(cls):
        # easy enough
        return None


    @classmethod
    def setDefaultDevice(cls, device):
        # ignore
        return None


    # metamethods
    def __init__(self, **kwds):
        # absorb all
        return


    def __bool__(self):
        """
        Simplify state testing
        """
        return self.state


    # implementation details
    def commit(self):
        """
        Commit my payload to the journal
        """
        # do nothing
        return self


    # constant
    severity = "null"     # the channel severity


# end of file
