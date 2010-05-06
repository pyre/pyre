# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Function import Function


class Binary(Function):
    """
    Base class for evaluators that are functions of two nodes
    """


    # interface
    def getDomain(self):
        """
        Iterate over my domain
        """
        # yield my two operands
        yield self._op1
        yield self._op2
        return


    # meta methods
    def __init__(self, op1, op2, **kwds):
        super().__init__(**kwds)
        self._op1 = op1
        self._op2 = op2
        return


    # implementation details
    def _replace(self, name, old, new):
        """
        Patch my domain by replacing {old} with {new}.

        This is used by the model during node resolution. Please don't use directly unless you
        have thought the many and painful implications through
        """
        # check op1
        if old == self._op1:
            self._op1 = new
            return
        # check op2
        if old == self._op2:
            self._op2 = new
            return
        # else
        raise Firewall()
            

# end of file 
