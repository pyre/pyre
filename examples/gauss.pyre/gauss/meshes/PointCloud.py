# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import pyre


class PointCloud(pyre.interface, family="gauss.meshes"):
    """
    Interface declarator for an unstructured collection of points
    """


    # my default implementation
    @classmethod
    def default(cls):
        """
        The default {PointCloud} implementation
        """
        # use the built in random number generator
        from .Mersenne import Mersenne
        return Mersenne


    # interface
    @pyre.provides
    def points(self, count, box):
        """
        Build and return {count} random points from the interior of {box}
        """


# end of file 
