# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
from .. import disktypes

# superclass
from .IQ import IQ


# a radar sample made out of two int16 counts
class IQInt16(IQ):
    """
    The type specification of radar samples with {int16_t} counts
    """

    # constants
    ctype = "pyre::memory::iq_t<std::int16_t>"
    htype = disktypes.iqInt16
    count = disktypes.int16


# the singleton
iqInt16 = IQInt16()


# end of file
