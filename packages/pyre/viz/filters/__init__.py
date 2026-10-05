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


@pyre.foundry(implements=filter, tip="the filter that sorts a signal into geometric bins")
def geometric():
    """
    The filter that sorts a signal into bins whose widths grow geometrically
    """
    # pull the implementation
    from .Geometric import Geometric

    # and publish it
    return Geometric


@pyre.foundry(implements=filter, tip="the filter that maps magnitudes onto a sawtooth")
def logsaw():
    """
    The filter that maps magnitudes onto a sawtooth that repeats at every doubling
    """
    # pull the implementation
    from .LogSaw import LogSaw

    # and publish it
    return LogSaw


@pyre.foundry(implements=filter, tip="the filter that maps phases onto a sawtooth")
def polarsaw():
    """
    The filter that maps phases onto a sawtooth that repeats every twelfth of a turn
    """
    # pull the implementation
    from .PolarSaw import PolarSaw

    # and publish it
    return PolarSaw


@pyre.foundry(implements=filter, tip="the filter that sorts a signal into uniform bins")
def uniform():
    """
    The filter that sorts a signal into bins of equal width
    """
    # pull the implementation
    from .Uniform import Uniform

    # and publish it
    return Uniform


# end of file
