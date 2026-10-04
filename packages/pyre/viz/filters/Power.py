# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Filter import Filter


# the filter that applies a power law
class Power(pyre.flow.factory, family="pyre.viz.filters.power", implements=Filter):
    """
    The filter that maps each value {z} of a signal to {scale * (z / mean)^exponent}
    """

    # user configurable state
    mean = pyre.properties.float()
    mean.default = 1
    mean.doc = "the value that the signal is measured against"
    scale = pyre.properties.float()
    scale.default = 1
    scale.doc = "the overall scale of the output"
    exponent = pyre.properties.float()
    exponent.default = 1
    exponent.doc = "the exponent of the power law"

    # the input
    signal = pyre.viz.tile.input()
    signal.doc = "the input signal"

    # the output
    power = pyre.viz.tile.output()
    power.doc = "the signal after the power law"


# end of file
