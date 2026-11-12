# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
from .. import disktypes

# superclass
from .IQ import IQ


# a radar sample made out of two uint32 counts
class IQUInt32(IQ):
    """
    The type specification of radar samples with {uint32_t} counts
    """

    # constants
    ctype = "pyre::memory::iq_t<std::uint32_t>"  # my spelling in c++
    htype = disktypes.iqUInt32  # my hdf5 type, for the samples pyre writes
    count = disktypes.uint32  # the hdf5 type of each count


# the singleton
iqUInt32 = IQUInt32()


# end of file
