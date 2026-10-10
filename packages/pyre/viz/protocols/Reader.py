# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the specifications of my slots
from .Raster import Raster


# the protocol of the factories that open files
class Reader(pyre.flow.producer, family="pyre.viz.readers"):
    """
    The reader protocol: open the file at {uri} and expose the cells of a dataset in it as a
    raster; that is all a reader nobody knows anything about can promise
    """

    # user configurable state
    uri = pyre.properties.uri()
    uri.doc = "the location of the file to open"

    # the output
    raster = Raster.output()
    raster.doc = "the cells of a dataset in the file"


# end of file
