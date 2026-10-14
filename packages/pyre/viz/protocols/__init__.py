# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the specifications of the products
# the products that hold numbers
from .Quantity import Quantity as quantity

# tiles
from .Tile import Tile as tile

# refined by what their cells hold
from .Complex import Complex as complex
from .Real import Real as real
from .Magnitude import Magnitude as magnitude
from .Unit import Unit as unit
from .Channel import Channel as channel

# scalars
from .Scalar import Scalar as scalar

# the cells of a dataset
from .Raster import Raster as raster

# what a reader found in its file, and one of the datasets in it
from .Contents import Contents as contents
from .Dataset import Dataset as dataset

# and the encoded images
from .Image import Image as image

# the protocols of the factories
from .Accessor import Accessor as accessor
from .Filter import Filter as filter
from .Operator import Operator as operator
from .Colormap import Colormap as colormap
from .Normalizer import Normalizer as normalizer
from .Encoder import Encoder as encoder
from .Slicer import Slicer as slicer
from .Reader import Reader as reader
from .Picker import Picker as picker

# end of file
