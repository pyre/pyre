# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre
from pyre.components.Component import Component
from ..interfaces.Shape import Shape


class Box(Component, family="gauss.shapes.box", implements=Shape):
    """
    A representation of the interior of a box in $d$ dimensions
    """

    # public state
    # the center of the box
    diagonal = pyre.components.array()
    diagonal.doc = "a vector that specifies the major diagonal of the box"
    diagonal.default = ((0, 0), (1,1)) # default: the unit square


    # interface
    @pyre.components.export
    def contains(self, points):
        """
        Filter out the members of {points} that are exterior to this box
        """
        # form the list of intervals along each coördinate axis
        intervals = tuple(zip(*self.diagonal))
        # for each point
        for point in points:
            # for each coördinate
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


# end of file 
