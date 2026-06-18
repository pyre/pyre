# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the L-band product base and the shared geocoded group
from ..mixins.common import lsar
from ..mixins.geo import geoCoordinates

# my parts
from .Identification import Identification


# the NISAR Geocoded Single Look Complex product
class GSLC(lsar):
    """
    The GSLC product specification
    """

    # specialize the identification with the fixed product type
    identification = Identification()
    identification.doc = "the identification metadata"

    # the product group at /science/LSAR/GSLC, in geocoded coordinates
    GSLC = geoCoordinates()
    GSLC.doc = "the GSLC product data, in geocoded geometry"


# end of file
