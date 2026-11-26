# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Dimension import Dimension


# declaration
class Inferred(Dimension):
    """
    A chart axis whose tick marks are the unique values found in a given sheet column
    """

    # types
    from .InferredAxis import InferredAxis as axis

    # meta-methods
    def __get__(self, chart, cls):
        """
        Collect the rows of the sheet of {chart} by the value of my measure, or return myself when
        accessed through its class
        """
        # if I am being accessed through the class
        if chart is None:
            # return myself
            return self
        # otherwise, bin my measure over the chart and return it
        return self.axis(chart=chart, dimension=self)


# end of file
