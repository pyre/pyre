# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#

class PointCloud(object):
    """
    The abstract base class for point generators
    """


    # interface
    def points(self, n, box):
        """
        Generate {n} random points on the interior of {box}
        
        parameters: 
            {n}: the number of points to generate
            {box}: a pair of points on the plane that specify the major diagonal of the
                   rectangular region
        """
        raise NotImplementedError(
            "class {.__name__!r} should implement 'points'".format(type(self)))


# end of file 
