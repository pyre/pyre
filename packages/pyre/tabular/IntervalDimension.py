# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from collections import defaultdict
from .Dimension import Dimension


class IntervalDimension(Dimension):
    """
    The base class for binning data based on a descritization of a float interval
    """


    # public data
    interval = None
    subdivisions = None


    # types
    class bin:
        """
        The inferred dimension bin handler
        """

        # public data
        start = end = width = None
        subdivisions = None
        intervals = None
        rejects = None

        # interface
        @property
        def bins(self):
            # iterate over my intervals
            for n in range(self.subdivisions):
                # build the interval end points
                start = n * self.width
                end = start + self.width
                # yield the interval info and the contents of the matching bin
                yield (start, end), self.intervals[n]
            # all done
            return
                
        def initialize(self):
            """
            Prepare to receive and bin data
            """
            # create storage for my interval bins
            self.intervals = tuple(set() for n in range(self.subdivisions))
            self.rejects = set()
            # and return
            return

        def project(self, record, rank):
            """
            Extract my measure from {record} and decide which bin to place its {rank}
            """
            # get the value
            value = record[self.offset]
            # bin the record
            bin = int((value - self.start) // self.width)
            # check whether the value falls with my range
            if bin < 0 or bin >= self.subdivisions:
                # got a reject
                self.rejects.add(rank)
            # otherwise
            else:
                # place the rank in the appropriate bin
                self.intervals[bin].add(rank)
            # all done 
            return
        
        # meta methods
        def __init__(self, offset, interval, subdivisions, **kwds):
            super().__init__(**kwds)
            self.offset = offset
            self.start, self.end = interval
            self.subdivisions = subdivisions
            self.width = (self.end - self.start) / subdivisions
            return
            

    # interface
    def pyre_register(self, chart):
        """
        Build a bin handler for a newly built {chart}
        """
        return self.bin(offset=self.offset, interval=self.interval, subdivisions=self.subdivisions)


    # meta methods
    def __init__(self, interval, subdivisions, **kwds):
        super().__init__(**kwds)
        self.interval = interval
        self.subdivisions = subdivisions

        return


# end of file 
