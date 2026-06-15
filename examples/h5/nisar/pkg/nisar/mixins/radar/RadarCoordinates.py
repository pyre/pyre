# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the framework, through the {nisar} namespace
from nisar import h5

# my parts
from .Swaths import Swaths


# the radar-geometry product group
class RadarCoordinates(h5.schema.group):
    """
    The data group shared by all radar-geometry products: RSLC, RIFG, RUNW, ROFF

    Its imagery lives in the natural radar acquisition geometry, gathered under a
    {swaths} group. A product mounts one of these as its product group, e.g.
    /science/LSAR/RSLC.

    FIRST PASS: the {swaths} imagery below is SLC-specific. When the non-SLC radar
    products (RIFG/RUNW/ROFF) are added, the imagery moves into product-specific
    subclasses and this class retains only the shared radar coordinate framing.
    """

    # the radar-geometry imagery, by frequency
    swaths = Swaths()
    swaths.doc = "the radar-geometry imagery, organized by frequency"


# end of file
