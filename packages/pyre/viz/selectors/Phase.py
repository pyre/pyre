# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Selector import Selector


# the selector of the phase of a complex signal
class Phase(pyre.flow.factory, family="pyre.viz.selectors.phase", implements=Selector):
    """
    The selector that extracts the phase of each sample of a complex signal
    """

    # the input
    signal = pyre.viz.tile.input()
    signal.doc = "the input signal, a stream of complex values"

    # the output
    phase = pyre.viz.tile.output()
    phase.doc = "the phase of each sample"


# end of file
