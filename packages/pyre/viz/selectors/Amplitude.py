# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Selector import Selector


# the selector of the amplitude of a complex signal
class Amplitude(pyre.flow.factory, family="pyre.viz.selectors.amplitude", implements=Selector):
    """
    The selector that extracts the amplitude of each sample of a complex signal
    """

    # the input
    signal = pyre.viz.tile.input()
    signal.doc = "the input signal, a stream of complex values"

    # the output
    amplitude = pyre.viz.tile.output()
    amplitude.doc = "the amplitude of each sample"


# end of file
