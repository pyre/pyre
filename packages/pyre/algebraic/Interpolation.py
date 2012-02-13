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


    # public data
    formula = None # the expression supplied by the client


    # interface
    def getValue(self):
        """
        Compute and return my value
        """


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        return


    # private data


# end of file
