# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Unary import Unary


class Reference(Unary):
    """
    Refer to another node
    """


    # interface
    def eval(self):
        """
        Compute and return my value
        """
        return self._op.value


# end of file 
