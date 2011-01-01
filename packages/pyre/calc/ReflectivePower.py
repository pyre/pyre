# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Unary import Unary


class ReflectivePower(Unary):
    """
    Raise the value of a node to an exponent
    """


    def compute(self):
        """
        Compute and return my value
        """
        return self._base ** self._op.value


    # meta-methods
    def __init__(self, base, **kwds):
        super().__init__(**kwds)
        self._base = base
        return


# end of file 
