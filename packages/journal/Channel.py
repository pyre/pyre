# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import collections


# local types
from .Console import Console as console


# super-classes
from pyre.patterns.Named import Named


# declaration
class Channel(Named):
    """
    This class encapsulates access to the shared channel state
    """


    # class data
    defaultDevice = console(name="journal.console")


    # public data
    @property
    def active(self):
        """
        Get my current activation state
        """
        return self._inventory.state


    @active.setter
    def active(self, state):
        """
        Set my current activation state
        """
        # save the new state
        self._inventory.state = state
        # and return
        return


    @property
    def device(self):
        """
        Get my current output device
        """
        # first, check the specific device assigned to my channel
        device = self._inventory.device
        # if one was assigned, return it
        if device is not None: return device
        # otherwise, issue a request for the default device
        return self.defaultDevice


    @device.setter
    def device(self, device):
        """
        Associate a device to be used for my output
        """
        # attach the new device to my shared state
        self._inventory.device = device
        # and return
        return


    # meta methods
    def __init__(self, name, **kwds):
        # chain to my ancestors
        super().__init__(name=name, **kwds)
        # look up my shared state
        self._inventory = self._index[name]
        # and return
        return


    # implementation details
    # private class data
    # subclasses must supply a non-trivial implementation of the mechanism by which state
    # shared among channel instances is managed. the pure python implementation that this
    # package defaults to when the C++ extension is not available, uses a {defaultdict}; this
    # implies that we need access to a factory that builds instance with the correct default
    # activation state, hence the two nested class declaration below
    _index = None 

    # two classes for the configurable bits of channels. their names reflect their default
    # state, in the absence of any configuration instructions by the user. when the state is
    # False, the channel does not produce any output; when the device is {None}, the default
    # device is used instead
    class Enabled:
        """Shared state for channels that are enabled by default"""
        state = True
        device = None

    class Disabled:
        """Shared state for channels that are disabled by default"""
        state = False
        device = None


# end of file 
