# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class PointCloud(object):
    """
    The abstract base class for point generators
    """

    # interface
    def point(self, box):
        """
        Generate a random point on the interior of {box}
        
        parameters: 
            {box}: a pair of points on the plane that specify the major diagonal of the
                   rectangular region
        """
        raise NotImplementedError(
            "class {.__name__!r} should implement 'point'".format(type(self)))


# end of file 
