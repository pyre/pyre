# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node
from ..algebraic.Leaf import Leaf


class Variable(Leaf, Node):
    """
    Encapsulation of expression nodes that can hold a value.

    This is the main class exposed by this package.
    """


    # public data
    @property
    def value(self):
        """
        Return my value
        """
        # easy enough
        return self._value


    @value.setter
    def value(self, value):
        """
        Set my value to {value} and notify my observers
        """
        # update my value
        self._value = value
        # notify whomever is listening
        self.notifyObservers()
        # and return
        return


    # meta methods
    def __init__(self, value=None, **kwds):
        super().__init__(**kwds)
        self._value = value
        return


# end of file 
