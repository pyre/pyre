# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import operator, functools

import pyre
from .Shape import Shape


class Ball(pyre.component, family="gauss.shapes.ball", implements=Shape):
    """
    A representation of the interior of a sphere in $d$ dimensions
    """

    # public state
    # the radius of the ball
    radius = pyre.properties.float(default=1) # default: a unit sphere
    radius.doc = "the radius of the ball"

    # the center of the ball
    center = pyre.properties.array(default=(0,0)) # default: centered at the origin
    center.doc = "the center of the ball"

    # interface
    @pyre.export
    def measure(self):
        """
        Compute my volume
        """
        # get #@$\pi$@
        from math import pi
        # compute the dimension of space
        d = len(self.center)
        # branch on even/odd d
        # for even d
        if d%2 == 0:
            normalization = functools.reduce(operator.mul, range(1, d//2+1))
            # compute the volume
            return pi**(d//2) * self.radius**d / normalization
        # for odd d
        normalization = functools.reduce(operator.mul, range(1, d+1, 2))
        # compute the volume
        return 2**((d+1)//2) * pi**((d-1)//2) / normalization

    @pyre.export
    def contains(self, points):
        """
        Filter out the members of {points} that are exterior to this ball
        """
        # cache the center of the ball
        center = self.center
        # compute the radius squared
        r2 = self.radius**2
        # for each point
        for point in points:
            # compute distance from the center
            d2 = sum((p - r)**2 for p,r in zip(point,center))
            # check whether this point is inside or outside
            if r2 >= d2:
                yield point
        # all done
        return


# end of file 
