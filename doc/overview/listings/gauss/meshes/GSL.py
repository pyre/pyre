# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre, itertools, gsl
from .PointCloud import PointCloud

class GSL(pyre.component, family="gauss.meshes.gsl", implements=PointCloud):
    """
    A point generator implemented using the large set of random number
    generators available as part of the gnu scientific library (GSL)
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
            yield tuple(itertools.starmap(self.rng.uniform, intervals))
            # update the counter
            n -= 1
        # all done
        return


# end of file 
