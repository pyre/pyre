# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Accessor import Accessor as accessor


# the implementations
@pyre.foundry(implements=accessor, tip="the accessor of the imaginary part of a complex signal")
def imaginary():
    """
    The accessor of the imaginary part of a complex signal
    """
    # pull the implementation
    from .Imaginary import Imaginary

    # and publish it
    return Imaginary


@pyre.foundry(implements=accessor, tip="the accessor of the real part of a complex signal")
def real():
    """
    The accessor of the real part of a complex signal
    """
    # pull the implementation
    from .Real import Real

    # and publish it
    return Real


# end of file
