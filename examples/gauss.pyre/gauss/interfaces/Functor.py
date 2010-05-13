# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre
from pyre.components.Interface import Interface

class Functor(Interface):
    """
    Facility declaration for function objects
    """

    # interface
    @pyre.components.provides
    def eval(self, points):
        """
        Evaluate the function at the supplied points
        """


# end of file 
