# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Filter import Filter


# the filter that maps phases onto a sawtooth that repeats every twelfth of a turn
class PolarSaw(pyre.flow.factory, family="pyre.viz.filters.polarsaw", implements=Filter):
    """
    The filter that maps each value of a signal of phases to the fractional part of its
    measure in units of pi/6, a sawtooth in [0,1) that repeats every twelfth of a turn
    """

    # the input
    signal = pyre.viz.tile.input()
    signal.doc = "the input signal, a stream of phases"

    # the output
    polarsaw = pyre.viz.tile.output()
    polarsaw.doc = "the sawtooth, in [0,1)"


# end of file
