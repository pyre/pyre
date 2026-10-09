# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre


# the protocol of what a reader makes of a file
class Datasets(pyre.flow.specification, family="pyre.viz.datasets"):
    """
    The datasets a reader found in a file, from which a selector picks the one to look at
    """


# end of file
