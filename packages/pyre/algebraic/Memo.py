# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# we build weak references to nodes
import weakref


# class declaration
class Memo:
    """
    A mix-in class that implements value memoization
    """


    # interface
    def getValue(self):
        """
        Override the node value retriever and return the contents of my value cache if it is up
        to date; otherwise, recompute the value and update the cache
        """
        # if my cache is invalid
        if self._value is None:
            # recompute
            self._value = super().getValue()
        # return the cache contents
        return self._value


    def setValue(self, value):
        """
        Override the value setter to invalidate my cache and notify my observers
        """
        # invalidate my cache and notify my observers
        self.flush()
        # update the value
        super().setValue(value=value)
        # and return
        return


    def flush(self):
        """
        Invalidate my cache and notify my observers
        """
        # do nothing if my cache is already invalid
        if self._value is None: return

        # invalidate the cache
        self._value = None

        # initialize the list of dead references
        dead = []
        # notify my observers
        for noderef in self.observers:
            # get the node
            node = noderef()
            # if it is still alive
            if node is not None:
                # flush it
                node.flush()
            # otherwise
            else:
                # put its reference on the discard pile
                dead.append(noderef)
        # clean up
        for ref in dead: self.observers.remove(ref)

        # and return
        return


    # meta methods
    def __init__(self, operands=(), **kwds):
        super().__init__(operands=operands, **kwds)

        # initialize the set of my observers
        self.observers = set()
        # add me as an observer to each of my operands
        for operand in operands: operand.observers.add(weakref.ref(self))

        # and return
        return


    # private data
    _value = None


# end of file 
