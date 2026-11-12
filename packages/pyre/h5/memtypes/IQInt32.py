# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
from .. import disktypes

# superclass
from .IQ import IQ


# a radar sample made out of two int32 counts
class IQInt32(IQ):
    """
    The type specification of radar samples with {int32_t} counts
    """

    # constants
    ctype = "pyre::memory::iq_t<std::int32_t>"
    htype = disktypes.iqInt32
    count = disktypes.int32


# the singleton
iqInt32 = IQInt32()


# end of file
