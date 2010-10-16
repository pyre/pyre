# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..patterns.Named import Named


class Measure(Named):
    """
    The base class for table descriptors
    """


    # algebra
    def __add__(self, other):
        return type(self)()


    def __radd__(self, other):
        return type(self)()


    def __sub__(self, other):
        return type(self)()


    def __rsub__(self, other):
        return type(self)()


    def __mul__(self, other):
        return type(self)()


    def __truediv__(self, other):
        return type(self)()


# end of file 
