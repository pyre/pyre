# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from .Filter import Filter


# the filter that maps [0,1] onto an interval
class Affine(pyre.flow.factory, family="pyre.viz.filters.affine", implements=Filter):
    """
    The filter that maps the values of a signal in [0,1] linearly onto its {interval}
    """

    # user configurable state
    interval = pyre.properties.tuple(schema=pyre.properties.float(), default=(0, 1))
    interval.doc = "the interval that [0,1] maps onto"

    # the input
    signal = pyre.viz.tile.input()
    signal.doc = "the input signal, a stream of values in [0,1]"

    # the output
    affine = pyre.viz.tile.output()
    affine.doc = "the signal mapped onto {interval}"


# end of file
