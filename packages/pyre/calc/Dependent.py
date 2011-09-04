# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from ..algebraic.Composite import Composite


class Dependent(Composite):
    """
    This class maintains the tuple of nodes that form the dependencies of its instances
    """

    
    # interface
    def flush(self, node=None):
        """
        Invalidate my value cache and notify my observers
        """
        # N.B.: there is another copy of this method in {Expression}
        # bail out if I am already marked as invalid
        if self._value is None: return
        # otherwise, invalidate my cache
        self._value = None
        # notify my observers
        self.notifyObservers()
        # and return
        return self


    # meta methods
    def __init__(self, operands, **kwds):
        super().__init__(**kwds)
        # keep a record of the nodes i depend on
        self._operands = operands
        # add me as their observer
        for operand in operands: operand.addObserver(self.flush)
        # all done
        return


    # private data
    _value = None # my value cache



# end of file 
