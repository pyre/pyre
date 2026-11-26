# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import math

# superclass
from .Dimension import Dimension


# declaration
class Interval(Dimension):
    """
    A chart axis whose tick marks are intervals of (a subset) of the range of the values in a
    given sheet column.
    """

    # meta-methods
    def __get__(self, chart, cls):
        """
        Bin my measure over the sheet of {chart}, or return myself when accessed through its class
        """
        # if I am being accessed through an instance
        if chart:
            # bin my measure over the chart and return it
            return self.axis(chart=chart, dimension=self)
        # otherwise, just return myself
        return self

    # meta-methods
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

    # implementation details
    class axis:
        """
        The bins of an interval over the sheet of a chart, and the rows that fall outside it
        """

        # meta-methods
        def __init__(self, chart, dimension, **kwds):
            """
            Bin the values of the measure of {dimension} over the sheet of {chart}
            """
            # chain up
            super().__init__(**kwds)

            # get the sheet
            sheet = chart.sheet
            # the measure
            measure = dimension.measure
            # and my column number
            column = sheet.pyre_columns[measure]

            # the range of my bins
            start, end = dimension.interval
            # their number
            subdivisions = dimension.subdivisions
            # and their width
            width = (end - start) / subdivisions

            # build my bins
            self.bins = tuple(set() for bin in range(subdivisions))
            # and a list of records that were rejected because they are outside my interval
            self.rejects = []

            # get the records
            for row, record in enumerate(sheet.pyre_data):
                # get the value of my measure
                value = record[column]
                # find its bin; values below the start rank below the first bin
                rank = math.floor((value - start) / width)
                # check whether it falls within my bounds
                if 0 <= rank < subdivisions:
                    # place it in its bin
                    self.bins[rank].add(row)
                # otherwise
                else:
                    # reject it
                    self.rejects.append(row)

            # all done
            return

        def __len__(self):
            """
            Count my bins
            """
            # easy enough
            return len(self.bins)

        def __iter__(self):
            """
            Build an iterator over my bins
            """
            # also easy
            return iter(self.bins)

        def __getitem__(self, bin):
            """
            Retrieve the set of rows in {bin}
            """
            # also easy
            return self.bins[bin]


# end of file
