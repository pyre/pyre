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
    ctype = "pyre::memory::iq_t<std::int8_t>"
    htype = disktypes.iqInt8
    count = disktypes.int8


# the singleton
iqInt8 = IQInt8()


# end of file
