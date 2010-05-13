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

        return


# end of file 
