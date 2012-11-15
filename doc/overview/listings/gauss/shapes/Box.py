# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import pyre
from .Shape import Shape

class Box(pyre.component, family="gauss.shapes.box", implements=Shape):
    """
    A representation of the interior of a $d$-dimensional box
    """
    # public state
    diagonal = pyre.properties.array(default=((0,0),(1,1)))
    diagonal.doc = "a vector that specifies the major diagonal of the box"

    # interface
    @pyre.export
    def measure(self):
        """
        Compute my volume
        """
        # externals
        import functools, operator
        # compute and return the volume
        return functools.reduce(
            operator.mul, ((right-left) for left,right in self.intervals()))

    @pyre.export
    def interior(self, points):
        """
        Filter out the members of {points} that are exterior to this box
        """
        # form the list of intervals alomg each cöordinate axis
        intervals = tuple(self.intervals()) # expand and store
        # now, for each point
        for point in points:
            # for each cöordinate
            for p, (left,right) in zip(point, intervals):
                # if this point is outside the box
                if p < left or p > right:
                    # move on to the next point
                    break
            # if we got here, all tests passed, so
            else:
                # this one is on the interior
                yield point
        # all done
        return

    # utilities
    def intervals(self):
        """
        Re-pack the diagonal vector as a list of the intervals along each axis
        """
        return zip(*self.diagonal)


# end of file 
