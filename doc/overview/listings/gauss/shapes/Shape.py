# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre

class Shape(pyre.interface, family="gauss.shapes"):
    """
    The obligations of implementations of geometrical shapes
    """

    # my default implementation
    @classmethod
    def default(cls):
        """
        The default {Shape} implementation
        """
        # use a box
        from .Box import Box
        return Box # if you return an instance, it will be shared by all...

    # required interface
    @pyre.provides
    def measure(self):
        """
        Compute my measure: length, area, volume, etc
        """
        
    @pyre.provides
    def interior(self, points):
        """
        Filter out {points} that are on my exterior
        """


# end of file 
