# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# products
from . import rasters
from . import tiles

# factories
from . import colormaps
from . import filters
from . import selectors
from . import codecs


# easy access to the protocols
# products
raster = rasters.raster
tile = tiles.tile
# factories
codec = codecs.codec
colormap = colormaps.colormap


# end of file
