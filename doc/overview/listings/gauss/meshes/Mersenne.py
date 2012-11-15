# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre, random, itertools
from .PointCloud import PointCloud

class Mersenne(pyre.component, family="gauss.meshes.mersenne",
               implements=PointCloud):
    """
    A point generator implemented using the Mersenne Twister random number
    generator that is available as part of the python standard library
    """

    # interface
    @pyre.export
    def points(self, n, box):
        """
        Generate {n} random points in the interior of {box}
        """
        # unfold the bounding box
        intervals = tuple(box.intervals()) # realize, so we can reuse in the loop
        # loop over the sample size
        while n > 0:
            # make a point and yield it
            yield tuple(itertools.starmap(random.uniform, intervals))
            # update the counter
            n -= 1
        # all done
        return


# end of file 
