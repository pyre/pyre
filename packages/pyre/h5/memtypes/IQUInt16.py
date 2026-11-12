# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
from .. import disktypes

# superclass
from .IQ import IQ


# a radar sample made out of two uint16 counts
class IQUInt16(IQ):
    """
    The type specification of radar samples with {uint16_t} counts
    """

    # constants
    ctype = "pyre::memory::iq_t<std::uint16_t>"
    htype = disktypes.iqUInt16
    count = disktypes.uint16


# the singleton
iqUInt16 = IQUInt16()


# end of file
