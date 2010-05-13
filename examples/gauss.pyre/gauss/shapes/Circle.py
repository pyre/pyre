# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre.components
from pyre.components.Component import Component
from ..interfaces.Shape import Shape


class Circle(Component, family="gauss.regions.circle", implements=Shape):
    """
    Component that implements a circle
    """

    # public state
    # the center of the circle
    center = pyre.components.array()
    center.doc = "the center of the circle"
    center.default = (0.0, 0.0)

    # the radius of the circle
    radius = pyre.components.float()
    radius.doc = "the radius of the circle"
    radius.default = 1.0

    # the box that defines the useful part of the circle
    box = pyre.components.array()
    box.doc = "a bounding box that masks the desired part of the circle"
    box.default = ((0,0), (1,1))


    # interface
    @pyre.components.export
    def contains(self, points):
        """
        Check whether each point in points is inside the circle
        """

        # compute the radius squared
        r2 = self.radius**2
        # unpack the circle center
        x0, y0 = self.center
        # for each point
        for (x, y) in points:
            # compute distance from the center
            d2 = (x - x0)**2 + (y - y0)**2
            # check whether this point is inside or outside
            if d2 > r2:
                yield False
            else:
                yield True

        return


# end of file 
