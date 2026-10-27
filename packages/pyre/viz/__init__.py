# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the protocols of the products and the factories
from . import protocols

# products
from . import images
from . import scalars
from . import tiles

# factories
from . import accessors
from . import readers
from . import colormaps
from . import encoders
from . import filters
from . import normalizers
from . import operators
from . import slicers

# easy access to the protocols
# of the products: encoded images
image = images.image
# the cells of datasets
raster = protocols.raster
# tiles
tile = tiles.tile
# scalars
scalar = scalars.scalar
# and either one
quantity = protocols.quantity
# of the factories: the parts of structured values
accessor = accessors.accessor
# the readers of datasets
reader = readers.reader
# the maps from values to colors
colormap = colormaps.colormap
# the encoders of images
encoder = encoders.encoder
# the filters
filter = filters.filter
# the normalizers
normalizer = normalizers.normalizer
# the operators
operator = operators.operator
# and the slicers of rasters into tiles
slicer = slicers.slicer


# end of file
