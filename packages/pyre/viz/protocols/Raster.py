# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre


# the protocol of the cells of a dataset
class Raster(pyre.flow.specification, family="pyre.viz.rasters"):
    """
    The cells of a dataset, as a reader exposes them, out of which a slicer cuts tiles; a raster
    is no tile: its shape is the dataset's, not the one a request asks for
    """


# end of file
