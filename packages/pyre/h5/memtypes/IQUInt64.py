# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
from .. import disktypes

# superclass
from .IQ import IQ


# a radar sample made out of two uint64 counts
class IQUInt64(IQ):
    """
    The type specification of radar samples with {uint64_t} counts
    """

    # constants
    ctype = "pyre::memory::iq_t<std::uint64_t>"  # my spelling in c++
    htype = disktypes.iqUInt64  # my hdf5 type, for the samples pyre writes
    count = disktypes.uint64  # the hdf5 type of each count


# the singleton
iqUInt64 = IQUInt64()


# end of file
