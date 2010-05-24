# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre
from pyre.components.Component import Component
from ..interfaces.Shape import Shape


class Ball(Component, family="gauss.shapes.ball", implements=Shape):
    """
    A representation of the interior of a sphere in $d$ dimensions
    """

    # public state
    # the center of the ball
    center = pyre.components.array()
    center.doc = "the center of the ball"
    center.default = (0.0, 0.0)

    # the radius of the ball
    radius = pyre.components.float()
    radius.doc = "the radius of the ball"
    radius.default = 1.0


    # interface
    @pyre.components.export
    def measure(self):
        """
        Compute my volume
        """
        # get functools and operator
        import operator
        import functools
        # get π
        from math import pi as π
        # compute the dimension of space
        d = len(self.center)
        # branch on even/odd d
        if d%2 == 0:
            # for even d
            normalization = functools.reduce(operator.mul, range(1, d//2+1))
            # compute the volume
            return π**(d//2) * self.radius**d / normalization
            
        # for odd d
        normalization = functools.reduce(operator.mul, range(1, d+1, 2))
        return 2**((d+1)//2) * π**((d-1)//2) / normalization


    @pyre.components.export
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
