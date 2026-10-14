# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the protocols of the products and the factories
from . import protocols

# products
from . import contents
from . import datasets
from . import images
from . import tiles

# factories
from . import readers
from . import pickers
from . import colormaps
from . import encoders
from . import filters
from . import normalizers
from . import operators
from . import selectors
from . import slicers

# easy access to the protocols
# products
dataset = datasets.dataset
image = images.image
raster = protocols.raster
tile = tiles.tile
# factories
reader = readers.reader
picker = pickers.picker
colormap = colormaps.colormap
encoder = encoders.encoder
filter = filters.filter
normalizer = normalizers.normalizer
operator = operators.operator
selector = selectors.selector
slicer = slicers.slicer


# end of file
