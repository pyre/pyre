# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre
import random
import itertools
from .PointCloud import PointCloud


class Mersenne(pyre.component, family="gauss.meshes.mersenne", implements=PointCloud):
    """
    A point generator that uses the python builtin random number generator
    """


    # interface
    @pyre.export
    def points(self, count, box):
        """
        Generate {count} random points chosen from the interior of {box}
        """
        # unpack the bounding box to form its extent along each of the coördinate axes
        intervals = tuple(box.intervals())
        # our random number generator
        generator = random.uniform
        # get starmap from itertools
        starmap = itertools.starmap
        # loop {count} times
        while count > 0:
            # decrement the counter
            count -= 1
            # build a point by calling the random number generator as many times as there are
            # dimensions in the box specification and send it along
            yield tuple(starmap(generator, intervals))
        # all done
        return


# end of file 
