# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import collections


# super-classes
from pyre.patterns.Named import Named


# declaration
class Debug(Named):
    """
    This is a sample documentation string for class Debug
    """


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


    # meta methods
    def __init__(self, name, **kwds):
        # chain to my ancestors
        super().__init__(name=name, **kwds)
        # look up my shared state
        self._inventory = self._index[name]
        # and return
        return


    # implementation details
    # types
    class _State:
        # public data
        state = False
        device = None


    # class private data
    _index = collections.defaultdict(_State)


# end of file 
