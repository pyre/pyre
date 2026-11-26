# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from . import measure


# declaration
class Dimension:
    """
    The base class for implementing data binning strategies
    """

    # public data
    measure = None  # the sheet descriptor to bin

    # meta-methods
    def __init__(self, measure, **kwds):
        """
        Bin the values of {measure}, a field of the sheet of my chart
        """
        # chain up
        super().__init__(**kwds)
        # save my measure
        self.measure = measure
        # all done
        return

    def __get__(self, chart, cls):
        """
        Return myself when accessed through the class of a chart; binning over a chart instance
        is the job of my subclasses
        """
        # if I am being accessed through the class
        if chart is None:
            # return myself
            return self
        # otherwise, get the journal
        import journal

        # and complain
        raise journal.firewall("pyre.tabular").log("dimensions can't operate on chart instances")


# end of file
