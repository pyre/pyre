# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre


class Shape(pyre.interface):
    """
    Interface declarator for geometrical regions
    """


    # interface
    @pyre.provides
    def measure(self):
        """
        Compute my measure (length, area, volume, etc)
        """


    @pyre.provides
    def contains(self, points):
        """
        Filter out {points} that are on my exterior
        """


# end of file 
