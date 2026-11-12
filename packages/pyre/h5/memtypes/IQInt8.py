# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
from .. import disktypes

# superclass
from .IQ import IQ


# a radar sample made out of two int8 counts
class IQInt8(IQ):
    """
    The type specification of radar samples with {int8_t} counts
    """

    # constants
    ctype = "pyre::memory::iq_t<std::int8_t>"  # my spelling in c++
    htype = disktypes.iqInt8  # my hdf5 type, for the samples pyre writes
    count = disktypes.int8  # the hdf5 type of each count


# the singleton
iqInt8 = IQInt8()


# end of file
