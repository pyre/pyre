# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre
from pyre.components.Interface import Interface


class Shape(Interface):
    """
    Interface declaration for integration regions
    """

    # interface
    @pyre.components.provides
    def measure(self):
        """
        Compute my measure
        """

    @pyre.components.provides
    def contains(self, points):
        """
        Filter out the subset of {points} that is exterior to the shape
        """


# end of file 
