# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Accessor import Accessor


# the accessor of the real part of a complex signal
class Real(pyre.flow.factory, family="pyre.viz.accessors.real", implements=Accessor):
    """
    The accessor that extracts the real part of each sample of a complex signal
    """

    # the input
    signal = pyre.viz.tile.input()
    signal.doc = "the input signal, a stream of complex values"

    # the output
    real = pyre.viz.tile.output()
    real.doc = "the real part of each sample"

    # the c++ templates whose instantiations do my work, when a recipe is staged
    pyre_engines = ("pyre::flow::factories::accessors::real_t",)


# end of file
