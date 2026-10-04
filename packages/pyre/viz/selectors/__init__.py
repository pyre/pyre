# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Selector import Selector as selector


# the implementations
@pyre.foundry(implements=selector, tip="the selector of the amplitude of a complex signal")
def amplitude():
    """
    The selector of the amplitude of a complex signal
    """
    # pull the implementation
    from .Amplitude import Amplitude

    # and publish it
    return Amplitude


@pyre.foundry(implements=selector, tip="the selector of the imaginary part of a complex signal")
def imaginary():
    """
    The selector of the imaginary part of a complex signal
    """
    # pull the implementation
    from .Imaginary import Imaginary

    # and publish it
    return Imaginary


@pyre.foundry(implements=selector, tip="the selector of the phase of a complex signal")
def phase():
    """
    The selector of the phase of a complex signal
    """
    # pull the implementation
    from .Phase import Phase

    # and publish it
    return Phase


@pyre.foundry(implements=selector, tip="the selector of the real part of a complex signal")
def real():
    """
    The selector of the real part of a complex signal
    """
    # pull the implementation
    from .Real import Real

    # and publish it
    return Real


# end of file
