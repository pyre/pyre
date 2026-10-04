# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Filter import Filter as filter


# the implementations
@pyre.foundry(implements=filter, tip="the filter that maps [0,1] onto an interval")
def affine():
    """
    The filter that maps [0,1] onto an interval
    """
    # pull the implementation
    from .Affine import Affine

    # and publish it
    return Affine


@pyre.foundry(implements=filter, tip="a source of a constant signal")
def constant():
    """
    A source of a constant signal
    """
    # pull the implementation
    from .Constant import Constant

    # and publish it
    return Constant


@pyre.foundry(implements=filter, tip="the filter that maps the phase of a signal onto an interval")
def cycle():
    """
    The filter that maps the phase of a complex signal onto an interval
    """
    # pull the implementation
    from .Cycle import Cycle

    # and publish it
    return Cycle


@pyre.foundry(implements=filter, tip="the filter that keeps every n-th sample")
def decimate():
    """
    The filter that keeps every n-th sample
    """
    # pull the implementation
    from .Decimate import Decimate

    # and publish it
    return Decimate


@pyre.foundry(implements=filter, tip="the filter that maps an interval onto [0,1]")
def parametric():
    """
    The filter that maps an interval onto [0,1]
    """
    # pull the implementation
    from .Parametric import Parametric

    # and publish it
    return Parametric


@pyre.foundry(implements=filter, tip="the filter that applies a power law")
def power():
    """
    The filter that applies a power law
    """
    # pull the implementation
    from .Power import Power

    # and publish it
    return Power


# end of file
