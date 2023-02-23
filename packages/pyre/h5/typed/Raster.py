# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# rasters are tied to non-scalar datasets
class Raster:
    """
    The manager of large multidimensional datasets
    """

    # properties

    # interface
    def getTile(self, origin, shape):
        """
        Fetch a data tile of the given {shape} from {origin}
        """

    def setTile(self, destination):
        """
        Store a data tile at destination
        """

    # metamethods
    def __init__(self, dataset, schema, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my data source
        self._dataset = dataset
        # and my schema
        self._schema = schema
        # make a pile for the cached modifications
        self._staged = []
        # all done
        return

    def __str__(self):
        # easy enough
        return "raster"


# end of file
