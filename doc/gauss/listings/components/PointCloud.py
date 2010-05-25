# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre
from pyre.components.Interface import Interface

class PointCloud(Interface):
    """
    An abstraction for an unstructured collection of points at which the integrand gets evaluated.
    """
    
    # interface
    @pyre.components.provides
    def points(self, count, box):
        """
        Return {count} random points from the interior of {box}
        """


# end of file 
