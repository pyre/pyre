# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the specifications of my slots
from .Contents import Contents


# the protocol of the factories that open files
class Reader(pyre.flow.producer, family="pyre.viz.readers"):
    """
    The reader protocol: open the file at {uri} and describe what is in it as its contents: the
    datasets it holds, and the axes that tell them apart
    """

    # user configurable state
    uri = pyre.properties.uri()
    uri.doc = "the location of the file to open"

    # the output
    contents = Contents.output()
    contents.doc = "the datasets in the file, and the axes that tell them apart"


# end of file
