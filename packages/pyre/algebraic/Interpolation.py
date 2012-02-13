# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class Interpolation:
    """
    Support for building evaluation graphs involving the values of nodes registered with a
    {SymbolTable} instance
    """


    # types
    from .exceptions import CircularReferenceError, UnresolvedNodeError


    # public data
    expression = None # the expression supplied by the client


    # interface
    def getValue(self):
        """
        Compute and return my value
        """
        # easy enough
        return self.node.getValue()


    # meta methods
    def __init__(self, expression, node, **kwds):
        super().__init__(**kwds)
        self.node = node
        self.expression = expression
        return


    # private data
    node = None # my evaluation node


# end of file
