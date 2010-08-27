# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre


class PointCloud(pyre.interface):
    """
    Interface declarator for an unstructured collection of points
    """


    # interface
    @pyre.provides
    def points(self, count, box):
        """
        Build and return {count} random points from the interior of {box}
        """


# end of file 
