# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import collections


# super-classes
from .Channel import Channel


# declaration
class Firewall(Channel):
    """
    This class is the implementation of the debug channel
    """


    # types
    from .exceptions import FirewallError


    # public data
    fatal = False
    severity = "firewall"


    # interface
    def log(self, message=None):
        """
        Record my message to my device
        """
        # first, record the entry
        super().log(message)
        # if firewalls are not fatal, return normally
        if notself.fatal: return self
        # otherwise, raise an exception
        raise self.FirewallError(firewall=self)
        

    # meta methods
    def __init__(self, name, **kwds):
        # chain to my ancestors
        super().__init__(name=name, inventory=self._index[name], **kwds)
        # and return
        return


    # implementation details
    # types
    class _State:
        # public data
        state = True
        device = None


    # class private data
    _index = collections.defaultdict(_State)


# end of file 
