# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
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
            "class '%s' should implement 'point'" % self.__class__.__name__)


# end of file 
