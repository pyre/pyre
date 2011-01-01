# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import pyre.tracking
from ..calc.Node import Node


class Slot(Node):
    """
    Storage for trait values
    """


    # constants
    DEFAULT_PRIORITY = (-1, -1)


    # interface
    def setValue(self, value, locator=None):
        """
        Set my value to {value} and notify my observers
        """
        # build a locator
        locator = locator if locator is not None else pyre.tracking.here(level=1)
        # update my history
        self._history.append((value, locator))
        # and get an ancestor to do the rest
        return super().setValue(value=value)

        
    def merge(self, other):
        """
        Transfer the information from {other} if its priority is higher or equal to mine
        """
        # if her priority is higher or equal
        if other._priority >= self._priority:
            # transfer the priority
            self._priority = other._priority
            # get an ancestor to transfer the node info
            super().merge(other)
        # all done
        return


    # meta methods
    def __init__(self, priority=None, locator=None, **kwds):
        super().__init__(**kwds)
        self._history = []
        self._locator = locator if locator is not None else pyre.tracking.here(level=1)
        self._priority = priority if priority is not None else self.DEFAULT_PRIORITY
        return


    # debugging support
    def dump(self):
        super().dump()
        if self._history:
            print("   history:")
            for value, priority, locator in self._history:
                print("     value: {!r}".format(value))
                print("     priority: {!r}".format(priority))
                print("     from: {!r}".format(locator))
        return


    # private data
    _priority = None
    _history = None


# end of file 
