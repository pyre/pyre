# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .MemoryType import MemoryType


# a complex number: a pair of reals
class Complex(MemoryType):
    """
    The base class of the type specifications of complex numbers
    """

    # constants
    # the disk type of each part
    part = None

    # interface
    def aligned(self, dataset):
        """
        My hdf5 type, with my parts lined up by position with the two members of {dataset} when
        it stores its cells as a compound, whatever the file calls them
        """
        # a dataset that stores pairs knows the names of its members
        if dataset.pairs:
            # so line my parts up with them
            return dataset.pair(count=self.part)
        # any other storage is converted by the library from my own type
        return self.htype


# end of file
