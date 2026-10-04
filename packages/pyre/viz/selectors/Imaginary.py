# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Selector import Selector


# the selector of the imaginary part of a complex signal
class Imaginary(pyre.flow.factory, family="pyre.viz.selectors.imaginary", implements=Selector):
    """
    The selector that extracts the imaginary part of each sample of a complex signal
    """

    # the input
    signal = pyre.viz.tile.input()
    signal.doc = "the input signal, a stream of complex values"

    # the output
    imaginary = pyre.viz.tile.output()
    imaginary.doc = "the imaginary part of each sample"


# end of file
