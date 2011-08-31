# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Polyadic import Polyadic


class Count(Polyadic):
    """
    Compute the number of nodes in my domain
    """


    def eval(self):
        """
        Compute and return my value
        """
        return len(self._domain)


# end of file 
