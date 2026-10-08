# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Filter import Filter


# the filter that maps magnitudes onto a sawtooth that repeats at every doubling
class LogSaw(pyre.flow.factory, family="pyre.viz.filters.logsaw", implements=Filter):
    """
    The filter that maps the magnitude of each sample to the fractional part of its base two
    logarithm, a sawtooth in [0,1) that repeats every time the magnitude doubles
    """

    # the input
    signal = pyre.viz.tile.input()
    signal.doc = "the input signal"

    # the output
    logsaw = pyre.viz.tile.output()
    logsaw.doc = "the sawtooth, in [0,1)"


# end of file
