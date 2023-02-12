# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# rasters are tied to non-scalar datasets
class Raster:
    """
    The manager of large multidimensional datasets
    """

    # metamethods
    def __init__(self, dataset, schema, **kwds):
        # chain up
        super().__init__(**kwds)
        # make a pile for the cached modifications
        self._staged = []
        # all done
        return

    def __str__(self):
        # easy enough
        return "<raster>"


# end of file
