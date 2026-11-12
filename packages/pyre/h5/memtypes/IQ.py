# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .MemoryType import MemoryType


# a radar sample: a pair of integer counts
class IQ(MemoryType):
    """
    The base class of the type specifications of radar samples, a pair of integer counts
    """

    # constants
    # the disk type of each count
    count = None

    # interface
    def aligned(self, dataset):
        """
        My hdf5 type, with my counts lined up with the two members of {dataset} by position,
        whatever the file calls them
        """
        # the dataset knows the names of its members
        return dataset.pair(count=self.count)


# end of file
