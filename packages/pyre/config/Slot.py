# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..calc.Node import Node


class Slot(Node):
    """
    Storage for trait values
    """


    # constants
    DEFAULT_PRIORITY = (-1, -1)


    # interface
    def merge(self, other):
        """
        Transfer the information from {other} if its priority is higher or equal to mine
        """
        # if her priority is higher or equal
        if other._priority >= self._priority:
            # shutdown my evaluator
            if self._evaluator:  self._evaluator.finalize(owner=self)
            # assume the attributes of other
            self._value = other._value
            self._evaluator = other._evaluator
            self._priority = other._priority
            # notify my observers
            self.notifyObservers()
        # all done
        return


    # meta methods
    def __init__(self, priority=None, **kwds):
        super().__init__(**kwds)
        self._history = []
        self._priority = priority if priority is not None else self.DEFAULT_PRIORITY
        return


    # private data
    _priority = None
    _history = None


# end of file 
