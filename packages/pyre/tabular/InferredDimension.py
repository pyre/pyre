# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from collections import defaultdict
from .Dimension import Dimension


class InferredDimension(Dimension):
    """
    The base class for binning data based on the discrete set of values assumed by some measure
    """


    # types
    class bin(defaultdict):
        """
        The inferred dimension bin handler
        """

        # interface
        @property
        def bins(self):
            return sorted(self.items())

        def initialize(self):
            """
            Prepare to receive and bin data
            """
            return

        def project(self, record, rank):
            """
            Extract my measure from {record} and decide which bin to place its {rank}
            """
            # get the value
            value = record[self.offset]
            # bin the record
            self[value].add(rank)
            # all done 
            return
        
        # meta methods
        def __init__(self, offset, **kwds):
            super().__init__(set, **kwds)
            self.offset = offset
            return
            

    # interface
    def pyre_register(self, chart):
        """
        Build a bin handler for a newly built {chart}
        """
        return self.bin(offset=self.offset)


# end of file 
