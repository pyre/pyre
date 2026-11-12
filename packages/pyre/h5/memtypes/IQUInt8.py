# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
from .. import disktypes

# superclass
from .IQ import IQ


# a radar sample made out of two uint8 counts
class IQUInt8(IQ):
    """
    The type specification of radar samples with {uint8_t} counts
    """

    # constants
    ctype = "pyre::memory::iq_t<std::uint8_t>"
    htype = disktypes.iqUInt8
    count = disktypes.uint8


# the singleton
iqUInt8 = IQUInt8()


# end of file
