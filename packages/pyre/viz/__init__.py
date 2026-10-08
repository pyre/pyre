# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the protocols of the products and the factories
from . import protocols

# products
from . import rasters
from . import tiles

# factories
from . import colormaps
from . import encoders
from . import filters
from . import normalizers
from . import operators
from . import selectors

# easy access to the protocols
# products
raster = rasters.raster
tile = tiles.tile
# factories
colormap = colormaps.colormap
encoder = encoders.encoder
filter = filters.filter
normalizer = normalizers.normalizer
operator = operators.operator
selector = selectors.selector


# end of file
