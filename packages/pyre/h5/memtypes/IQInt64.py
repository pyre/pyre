# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
from .. import disktypes

# superclass
from .IQ import IQ


# a radar sample made out of two int64 counts
class IQInt64(IQ):
    """
    The type specification of radar samples with {int64_t} counts
    """

    # constants
    ctype = "pyre::memory::iq_t<std::int64_t>"
    htype = disktypes.iqInt64
    count = disktypes.int64


# the singleton
iqInt64 = IQInt64()


# end of file
