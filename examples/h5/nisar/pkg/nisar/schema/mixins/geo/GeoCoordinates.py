# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework, through the {nisar} namespace
import nisar

# my parts
from .Grids import Grids


# the geocoded product group
class GeoCoordinates(nisar.h5.schema.group):
    """
    The data group shared by all geocoded products: GSLC, GUNW, GOFF, GCOV

    Its imagery is resampled onto a map projection grid, gathered under a {grids}
    group. A product mounts one of these as its product group, e.g.
    /science/LSAR/GSLC.

    FIRST PASS: the {grids} imagery below is SLC-specific. When the non-SLC
    geocoded products (GUNW/GOFF/GCOV) are added, the imagery moves into
    product-specific subclasses and this class retains only the shared geocoded
    coordinate framing.
    """

    # the geocoded imagery, by frequency
    grids = Grids()
    grids.doc = "the geocoded imagery, organized by frequency"


# end of file
