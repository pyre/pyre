# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Polyadic import Polyadic


class Average(Polyadic):
    """
    Compute the average of the nodes in my domain
    """


    def eval(self):
        """
        Compute and return my value
        """
        return sum(node.value for node in self._domain)/len(self._domain)


# end of file 
