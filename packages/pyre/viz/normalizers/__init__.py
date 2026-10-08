# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Normalizer import Normalizer as normalizer


# the implementations
@pyre.foundry(implements=normalizer, tip="the normalizer that maps an interval onto [0,1]")
def parametric():
    """
    The normalizer that maps an interval onto [0,1]
    """
    # pull the implementation
    from .Parametric import Parametric

    # and publish it
    return Parametric


# end of file
