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
from ..protocols.Magnitude import Magnitude


# the operator that computes the amplitude of a complex signal
class Amplitude(pyre.flow.factory, family="pyre.viz.operators.amplitude", implements=Unary):
    """
    The unary operator that computes the amplitude of each sample of a complex signal
    """

    # the input
    signal = Complex.input()
    signal.doc = "the input signal, a stream of complex values"

    # the output
    amplitude = Magnitude.output()
    amplitude.doc = "the amplitude of each sample"

    # the c++ templates whose instantiations do my work, when a recipe is staged
    pyre_engines = ("pyre::flow::factories::selectors::amplitude_t",)


# end of file
