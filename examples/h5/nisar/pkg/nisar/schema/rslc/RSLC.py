# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the L-band product base and the shared radar-geometry group
from ...mixins.common import lsar
from ...mixins.radar import radarCoordinates

# my parts
from .Identification import Identification


# the NISAR Range-Doppler Single Look Complex product
class RSLC(lsar):
    """
    The RSLC product specification
    """

    # specialize the identification with the fixed product type
    identification = Identification()
    identification.__doc__ = "the identification metadata"

    # the product group at /science/LSAR/RSLC, in radar coordinates
    RSLC = radarCoordinates()
    RSLC.__doc__ = "the RSLC product data, in radar geometry"


# end of file
