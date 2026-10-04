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
@pyre.foundry(implements=filter, tip="the filter that maps an interval onto [0,1]")
def parametric():
    """
    The parametric filter
    """
    # pull the implementation
    from .Parametric import Parametric

    # and publish it
    return Parametric


# end of file
