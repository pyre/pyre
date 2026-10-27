# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Operator import Operator as operator


# the implementations
@pyre.foundry(implements=operator, tip="the amplitude of each sample of a complex signal")
def amplitude():
    """
    The amplitude of each sample of a complex signal
    """
    # pull the implementation
    from .Amplitude import Amplitude

    # and publish it
    return Amplitude


@pyre.foundry(implements=operator, tip="the phase of each sample of a complex signal")
def phase():
    """
    The phase of each sample of a complex signal
    """
    # pull the implementation
    from .Phase import Phase

    # and publish it
    return Phase


@pyre.foundry(implements=operator, tip="the sum of two quantities")
def add():
    """
    The sum of two quantities
    """
    # pull the implementation
    from .Add import Add

    # and publish it
    return Add


@pyre.foundry(implements=operator, tip="the difference of two quantities")
def subtract():
    """
    The difference of two quantities
    """
    # pull the implementation
    from .Subtract import Subtract

    # and publish it
    return Subtract


@pyre.foundry(implements=operator, tip="the product of a tile and a scalar, or of two scalars")
def multiply():
    """
    The product of a tile and a scalar, or of two scalars
    """
    # pull the implementation
    from .Multiply import Multiply

    # and publish it
    return Multiply


@pyre.foundry(implements=operator, tip="the quotient of a tile or a scalar by a scalar")
def divide():
    """
    The quotient of a tile or a scalar by a scalar
    """
    # pull the implementation
    from .Divide import Divide

    # and publish it
    return Divide


# end of file
