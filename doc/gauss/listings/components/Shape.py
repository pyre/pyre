# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import pyre

class Shape(pyre.interface):
    """
    Interface declaration for integration regions
    """

    # interface
    @pyre.provides
    def measure(self):
        """
        Compute my measure
        """

    @pyre.provides
    def contains(self, points):
        """
        Filter out the subset of {points} that is exterior to the shape
        """


# end of file 
