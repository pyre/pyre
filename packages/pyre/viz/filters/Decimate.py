# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Filter import Filter


# the filter that keeps every n-th sample
class Decimate(pyre.flow.factory, family="pyre.viz.filters.decimate", implements=Filter):
    """
    The filter that thins a signal out by keeping one sample in every {2^level} along each
    axis
    """

    # user configurable state
    level = pyre.properties.int()
    level.default = 0
    level.doc = "the samples kept are {2^level} apart along each axis"

    # the input
    signal = pyre.viz.tile.input()
    signal.doc = "the input signal"

    # the output
    decimated = pyre.viz.tile.output()
    decimated.doc = "the samples that were kept"


# end of file
