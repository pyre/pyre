# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Dimension import Dimension


# declaration
class Interval(Dimension):
    """
    A chart axis whose tick marks are intervals of (a subset) of the range of the values in a
    given sheet column.
    """

    # types
    from .IntervalAxis import IntervalAxis as axis

    # meta-methods
    def __get__(self, chart, cls):
        """
        Bin my measure over the sheet of {chart}, or return myself when accessed through its class
        """
        # if I am being accessed through the class
        if chart is None:
            # return myself
            return self
        # otherwise, bin my measure over the chart and return it
        return self.axis(chart=chart, dimension=self)

    def __init__(self, interval, subdivisions, **kwds):
        """
        Split {interval}, a pair of its start and end, into {subdivisions} bins of equal width
        """
        # chain up
        super().__init__(**kwds)
        # save my range
        self.interval = interval
        # and the number of my bins
        self.subdivisions = subdivisions
        # all done
        return


# end of file
