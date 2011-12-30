# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import operator, functools

import pyre
from .Shape import Shape

class Box(pyre.component, family="gauss.shapes.box", implements=Shape):
    """
    A representation of the interior of a d-dimensional box
    """

    # public state
    # the center of the box
    diagonal = pyre.properties.array()
    diagonal.doc = "a vector that specifies the major diagonal of the box"
    diagonal.default = ((0, 0), (1,1)) # default: the unit square

    # component interface
    @pyre.export
    def measure(self):
        """
        Compute my volume
        """
        # compute and return the volume
        return functools.reduce(operator.mul, ((right-left) for left,right in self.sides()))

    @pyre.export
    def contains(self, points):
        """
        Filter out the members of {points} that are exterior to this box
        """
        # form the list of intervals along each coördinate axis
        intervals = tuple(self.sides())
        # now, for each point
        for point in points:
            # and for each coordinate
            for p,(left,right) in zip(point, intervals):
                # if it is outside the box interval
                if p < left or p > right:
                    # bail out and process the next point
                    break
            # if we got here, all the tests passed; so
            else:
                # this one is interior
                yield point
        # all done
        return

    # other interface
    def sides(self):
        """
        Repack the diagonal vector as a list of the intervals along each axis
        """
        return zip(*self.diagonal)


# end of file 
