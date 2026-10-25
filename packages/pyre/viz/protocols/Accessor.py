# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre


# the protocol for the accessors that extract a part of a complex signal
class Accessor(pyre.flow.producer, family="pyre.viz.accessors"):
    """
    The accessor protocol: extract one of the parts of a structured value
    """


# end of file
