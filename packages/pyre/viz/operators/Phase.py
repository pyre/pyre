# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Unary import Unary

# the specifications of my slots
from ..protocols.Complex import Complex
from ..protocols.Real import Real


# the operator that computes the phase of a complex signal
class Phase(pyre.flow.factory, family="pyre.viz.operators.phase", implements=Unary):
    """
    The unary operator that computes the phase of each sample of a complex signal
    """

    # the input
    signal = Complex.input()
    signal.doc = "the input signal, a stream of complex values"

    # the output
    phase = Real.output()
    phase.doc = "the phase of each sample"


# end of file
