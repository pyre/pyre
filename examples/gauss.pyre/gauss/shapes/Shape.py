# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre


class Shape(pyre.interface, family="gauss.shapes"):
    """
    Interface declarator for geometrical regions
    """


    # my default implementation
    @classmethod
    def default(cls):
        """
        The default {Shape} implementation
        """
        # use {Ball}
        from .Ball import Ball
        return Ball


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
