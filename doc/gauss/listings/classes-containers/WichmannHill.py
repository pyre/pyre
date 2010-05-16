# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import random
from PointCloud import PointCloud


class WichmannHill(PointCloud):
    """
    A point generator that is implemented using the Wichmann-Hill random number generator that
    is available as part of the python standard library
    """


    def points(self, n, box):
        """
        Generate {n{ random points in the interior of {box}
        """
        # create the container for the sample
        sample = []
        
        # unfold the bounding box
        intervals = tuple(zip(*box))
        
        # loop over the sample size
        while n > 0:
            p = [ random.uniform(left, right) for left,right in intervals ]
            sample.append(p)
            n -= 1
                
        return sample


# end of file 
