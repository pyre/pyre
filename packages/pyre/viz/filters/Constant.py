# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Filter import Filter


# a source of a constant signal
class Constant(pyre.flow.factory, family="pyre.viz.filters.constant", implements=Filter):
    """
    A source of a signal that has the same {value} everywhere, e.g. for the parts of a
    colormap that do not vary
    """

    # user configurable state
    value = pyre.properties.float()
    value.default = 0
    value.doc = "the value of every sample"

    # the output
    tile = pyre.viz.tile.output()
    tile.doc = "the constant signal"


# end of file
