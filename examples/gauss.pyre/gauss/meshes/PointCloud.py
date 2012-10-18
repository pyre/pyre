# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# access to the framework
import pyre


# declaration
class PointCloud(pyre.protocol, family="gauss.meshes"):
    """
    Protocol declarator for an unstructured collection of points
    """


    # my default implementation
    @classmethod
    def pyre_default(cls):
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
        Generate {count} random points on the interior of {box}
        parameters: 
            {count}: the number of points to generate
            {box}: a shape that defines the computational domain
        """


# end of file 
