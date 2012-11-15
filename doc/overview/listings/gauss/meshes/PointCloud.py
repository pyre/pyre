# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre

class PointCloud(pyre.interface, family="gauss.meshes"):
    """
    The abstract base class for point generators
    """

    # the default implementation
    @classmethod
    def default(cls):
        """
        The default {PointCloud} implementation
        """
        from .Mersenne import Mersenne
        return Mersenne

    # required interface
    @pyre.provides
    def points(self, n, box):
        """
        Generate {n} random points on the interior of {box}
        parameters: 
            {n}: the number of points to generate
            {box}: the major diagonal of the computational domain
        """


# end of file 
