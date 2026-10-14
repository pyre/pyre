# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Picker import Picker as picker


# the implementations
@pyre.foundry(implements=picker, tip="pick the dataset that matches a selection along every axis")
def match():
    """
    Pick the dataset of a file that matches a selection along every axis of its contents
    """
    # pull the implementation
    from .Match import Match

    # and publish it
    return Match


# end of file
